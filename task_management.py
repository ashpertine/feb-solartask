import heapq
import uuid
from datetime import datetime
#task is going to have the following: title, due_date, priority

PRIORITY_MAP = {"High": 1, "Medium": 2, "Low": 3}
class Task:
    def __init__ (self, title, due_date, priority):
        self.id = str(uuid.uuid4())
        self.title = title
        if isinstance(due_date, datetime):
            self.due_date = due_date
        else:
            self.due_date = datetime.strptime(due_date, '%d/%m/%Y')
        self.priority = priority

    #Compare priority
    def __lt__ (self, other): #dunder: less than
        return PRIORITY_MAP[self.priority] < PRIORITY_MAP[other.priority]
    
    def __gt__ (self, other): #dunder: greater than
        return PRIORITY_MAP[self.priority] > PRIORITY_MAP[other.priority]

#Binary Search Tree
class TaskNode: 
    def __init__(self, task):
        self.task = task
        self.task_list = [task] #store a list of tasks with same due_date in one node
        self.leftChild = None
        self.rightChild = None

class BSTTask:
    def __init__(self):
        self.root = None
    def insert(self, task):
        if self.root is None:
            self.root = TaskNode(task) #set the root to task
        else:
            self._insert_recursive(self.root, task)
            
    def _insert_recursive(self, node, task):
        if task.due_date < node.task.due_date: #earlier than node due date
            if node.leftChild is None:
                node.leftChild = TaskNode(task)
            else:
                self._insert_recursive(node.leftChild, task) #move down the tree
        elif task.due_date > node.task.due_date: #later than node due date
            if node.rightChild is None:
                node.rightChild = TaskNode(task)
            else: 
                self._insert_recursive(node.rightChild, task) #move down the tree
        else:
            node.task_list.append(task)
    
    
    def find_before_due_date(self, node, search_date):
        task_list = []
        def _search_bef(node, search_date):
            if node.task.due_date <= search_date: #earlier than search_date
                if len(node.task_list) > 1:
                    for task in node.task_list:
                        task_list.append(task)
                else:
                    task_list.append(node.task)
            if node.leftChild:
                _search_bef(node.leftChild, search_date)
            if node.rightChild:
                _search_bef(node.rightChild, search_date)
        _search_bef(node, search_date)
        return task_list
        
    def find_by_task(self, task):
        search_date = task.due_date
        def _find_by_date(node, search_date):
            if node is None:
                return 
            
            if node.task.due_date < search_date: #earlier than search date
                return _find_by_date(node.rightChild, search_date)
            elif node.task.due_date > search_date: #later than search date
                return _find_by_date(node.leftChild, search_date)
            elif node.task.due_date == search_date: #equal to search_date
                if len(node.task_list) > 1:
                    return node.task_list
                else:
                    return [node.task]
        tasks_with_date = _find_by_date(self.root, search_date)
        if len(tasks_with_date) > 1:
            new_task_list = self.match_id(tasks_with_date, task.id)
            if not new_task_list: #new_task_list is empty
                self.remove_node(search_date)
            else:
                self.update_node_task_list(search_date, new_task_list)
        else:
            self.remove_node(tasks_with_date)


    def match_id(self, task_list, target_task_id):
        for task in task_list:
            if task.id == target_task_id:
                task_list.remove(task)
        return task_list
    
    def update_node_task_list(self, search_date, new_task_list):
        if not new_task_list:
            return 
        def _update(node, search_date, new_task_list):
            if node is None:
                return 
            if node.task.due_date < search_date:
                return _update(node.rightChild, search_date, new_task_list)
            elif node.task.due_date > search_date:
                return _update(node.leftChild, search_date, new_task_list)
            else:
                node.task_list = new_task_list
                if new_task_list:
                    node.task = new_task_list[0]
        _update(self.root, search_date, new_task_list)

    def remove_node(self, tasks_with_date):
        target_date = tasks_with_date[0].due_date
        def _remove(node, date):
            if node is None:
                return None
            
            if node.task.due_date < date: #earlier than date
                return _remove(node.rightChild, target_date)
            elif node.task.due_date > date:
                return _remove(node.leftChild, target_date)
            else:
                #node is found
                if node.leftChild is None and node.rightChild is None:
                    return None
                elif node.leftChild is None:
                    return node.rightChild
                elif node.rightChild is None:
                    return node.leftChild
                else:
                    min_val = self.find_min(node.rightChild)
                    node.task = min_val
                    #remove successor node from the right subtree
                    node.rightChild = _remove(node.rightChild, target_date)
            return node
        self.root = _remove(self.root, target_date)

    
    #find minimum value by taking value of left most leaf
    def find_min(self, node):
        current = node
        while current.leftChild:
            current = current.leftChild
        return current

#completed list (linked list)
class ListNode:
    def __init__(self, task):
        self.task = task
        self.next = None
    
class CompletedLinkedList:
    def __init__(self):
        self.head = None

    def append(self, task):
        if self.head is None:
            self.head = ListNode(task)
        else:
            last = self.head #there is a starting node
            while last.next: #while the current node has a next node
                last = last.next #set the current node to the next node, and so on and so forth
            last.next = ListNode(task) #now there is no next node, so set the next node to the new node
    
    def delete(self, task):
        last = self.head
        if self.head is not None:
            if self.head.task.id == task.id: #if head is the target task, point to the next node
                self.head = self.head.next
                return True
            else:
                while last.next: 
                    if last.next.task.id == task.id: #found target node
                        last.next = last.next.next  #point the current node to the next node of the target node
                        print("linked list node deleted")
                        return True
        else:
            print("list is empty, nothing to delete")
            return False

    
    def get_history(self):
        history = []
        if self.head is None:
            return []
        elif self.head.next is None:
            return [self.head.task]
        else:
            last = self.head
            while last:
                history.append(last.task)
                last = last.next
        return history



class ManageTask:
    def __init__(self):
        self.task_map = {}
        self.priority_queue = []
        heapq.heapify(self.priority_queue)
        self.completed_task_history = CompletedLinkedList()
        self.undo_stack = []
        self.bst = BSTTask()
    
    def get_task(self):
       if not self.priority_queue:
           print("your task list is empty!")
       else:
           temp_heap = self.priority_queue[:]
           heapq.heapify(temp_heap)
           sorted_tasks = []
           while temp_heap:
                sorted_tasks.append(self.task_map[heapq.heappop(temp_heap)[1]])
           print(f'task_list: {sorted_tasks}')
           return sorted_tasks


    def add_task(self, task, undo_complete=False):
        self.task_map[task.id] = task
        heapq.heappush(self.priority_queue, (PRIORITY_MAP[task.priority], task.id))
        self.bst.insert(task)
        if undo_complete == False:
            self.undo_stack.append({
                "action": 'add_task',
                "task_obj": task,
                "delete_task": True
            })
        else:
            self.undo_stack.append({
                "action": "make_task_available",
                "task_obj": task,
                "delete_task": False
            })
        print(self.task_map)
        print(self.priority_queue)


    def complete_task(self, task_title):
        for tid, task in self.task_map.items():
            if task.title == task_title:
                task_id = tid 
                break
        if task_id in self.task_map:
            task = self.task_map.pop(task_id)
            self.priority_queue = [(p, tid) for p, tid in self.priority_queue if tid != task.id]
            heapq.heapify(self.priority_queue)
            try:
                self.bst.find_by_task(task)
            except ValueError:
                pass
            self.undo_stack.append({
                "action": 'complete_task',
                "task_obj": task
            })

            self.completed_task_history.append(task)
                
    def delete_task(self, task_title):
        for tid, task in self.task_map.items():
            if task.title == task_title:
                task_id = tid 
                break

        if task_id in self.task_map:
            task = self.task_map.pop(task_id)
            self.priority_queue = [(p, tid) for p, tid in self.priority_queue if tid != task.id]
            heapq.heapify(self.priority_queue)
            try:
                self.bst.find_by_task(task)
            except ValueError:
                pass
            self.undo_stack.append({
                "action": 'delete_task',
                "task_obj": task
            })

            print('successfully deleted!')

    def modify_task(self, task_title, **kwargs):
        for tid, task in self.task_map.items():
            if task.title == task_title:
                task_id = tid 
                break
            else:
                print('no task id with the title found!')
    
        if task_id in self.task_map:
            original_state = self.task_map[task_id]
            updated_state = Task(title=original_state.title, due_date=original_state.due_date, priority=original_state.priority)

            updated_state.id = original_state.id
            for key, value in kwargs.items():
                if key == 'new_title' and value:
                    setattr(updated_state, 'title', value)
                elif key == "new_due_date" and value:
                    setattr(updated_state, 'due_date', value)
                elif key == 'new_priority' and value:
                    setattr(updated_state, 'priority', value)
                else:
                    print(f"Invalid attribute for {key}")
        self.task_map[task_id] = updated_state
        self.priority_queue = [(p, tid) for p, tid in self.priority_queue if tid != task_id]
        heapq.heappush(self.priority_queue, (PRIORITY_MAP[updated_state.priority], task_id))
        #update bst: remove old task and insert the updated one.
        try:
            self.bst.find_by_task(original_state)
        except ValueError:
            pass
        self.bst.insert(updated_state)
        self.undo_stack.append({
            "action": "modify_task",
            "updated_task_obj": updated_state,
            "original_task_obj": original_state,
            "task_id": task_id
        })

    def undo(self):
        if len(self.undo_stack) == 0:
            print("nothing in undo stack!")
            return
        last_action = self.undo_stack.pop()
        print(last_action)
        if last_action['action'] == "add_task":
            task_title = last_action['task_obj'].title
            if last_action['delete_task'] == True:
                self.delete_task(task_title)
            
        elif last_action['action'] == "complete_task":
            task = last_action['task_obj']
            self.completed_task_history.delete(task)
            self.add_task(task, undo_complete=True)
            return
        elif last_action['action'] == 'make_task_available':
            task_title = last_action['task_obj'].title
            self.complete_task(task_title)
            return
        elif last_action['action'] == 'delete_task':
            task = last_action['task_obj']
            self.add_task(task)
            return
        elif last_action['action'] == 'modify_task':
            task = last_action['original_task_obj']
            new_task_title = last_action['updated_task_obj'].title
            self.modify_task(new_task_title, new_title=task.title, new_due_date=task.due_date, new_priority=task.priority)
            return
        else:
            print("invalid action!")
            
        

                






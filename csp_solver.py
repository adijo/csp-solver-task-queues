from collections import deque
import copy

class CSPSolver(object):
    """

    Class that encapsulates logic to solve an
    instance of the CSP problem.
    """

    def _ok(self, assignment_graph, source, value, target):
        """
        If source is assigned to target,
        is there any value that can be assigned 
        to target without violating the 
        constraint graph?
        """
        target_values = assignment_graph[target]
        return len(target_values - set([value])) > 0           


    def _possible(self, assignment_graph, assigned):
        for node in assignment_graph.keys():
            if node not in assigned and len(node) == 0:
                return False
        return True 

    def make_consistent(self, graph, assignment_graph, domains, variables, assigned):
        queue = deque()
        # populate the queue.
        for edge in graph:
            a, b = edge
            if a not in assigned and b not in assigned:
                queue.append((a, b))
                queue.append((b, a))
        #print assigned, queue, variables
        
        while queue:
            a, b = queue.popleft()
            # constraint is from a --> b
            a_values = assignment_graph[a]
            to_remove = set()
            for a_value in a_values:

                if not self._ok(assignment_graph, a, a_value, b):
                    to_remove.add(a_value)

                    # add back to queue the arcs that were 
                    # just made inconsistent.
                    for variable in variables:
                        if (variable, a) in graph:
                            queue.append((variable, a))
            # remove all values that are not good.
            a_values = a_values - to_remove
            if len(a_values) == 0:
                #print a, '-->', a_values
                #print "-----------------------"
                return False
        #print "ok"
        #print "----------------------------"
        return True


    def backtrack_search(self, variables, domains, graph, assignment_graph, assigned):
        if len(variables) == 0:
            return (True, assigned)
        else:
            if not self._possible(assignment_graph, assigned):
                return (False, None)
            else:
                current = variables.pop()
                possible_assignments = assignment_graph[current]
                
                for possible_assignment in possible_assignments:
                    assigned[current] = possible_assignment
                    #new_assignment = copy.deepcopy(possible_assignments) - set([possible_assignment])
                    #assignment_graph[current] = new_assignment
                    # current has been assigned possible_assignment temporarily.
                    new_assignment_graph = copy.deepcopy(assignment_graph)
                    for key in new_assignment_graph:
                        if (current, key) in graph or (key, current) in graph:
                            new_assignment_graph[key] = new_assignment_graph[key] - set([possible_assignment])
                    #print new_assignment_graph
                    #print assigned
                    consistent_possible = self.make_consistent(graph, new_assignment_graph, domains, variables, assigned)
                    if consistent_possible:
                        res = self.backtrack_search(variables, domains, graph, new_assignment_graph, assigned)
                        if res[0]:
                            return res
                    
                    del assigned[current]

                variables.append(current)
                #print "Can't assign value to ", current
                return (False, None)

    def build_assignment_graph(self, variables, domains, unary):
        # unary must be a dictionary of variables --> set of 
        # domains stuff that is not allowed.
        assignment_graph = {}
        for variable in variables:
            assignment_graph[variable] = set(domains) - unary[variable]
        return assignment_graph

    def solve(self, graph, variables, domains, unary):
        # the graph is a list of edges.
        assignment_graph = self.build_assignment_graph(variables, domains, unary)
        return self.backtrack_search(variables, domains, graph, assignment_graph, {})



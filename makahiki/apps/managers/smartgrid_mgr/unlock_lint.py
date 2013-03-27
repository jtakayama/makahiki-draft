'''Lint for DesignerAction unlock_conditions.
Based upon pyTree by caesar0301, https://github.com/caesar0301/pyTree

Created on Mar 26, 2013

@author: Cam Moore
'''
import uuid
from apps.widgets.smartgrid_design.models import DesignerAction

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)


def sanitize_string(s):
    return s.strip().replace(" ", "_")


class Node(object):
    """Node in unlock condition tree. Name is the slug of the action, parent is slug of
    condition dependance."""

    def __init__(self, name, unlock_condition, identifier=None, expanded=True):
        """initializer."""
        self.__identifier = (str(uuid.uuid1()) if identifier is None else
                             sanitize_string(str(identifier)))
        self.name = name
        self.unlock_condition = unlock_condition
        self.expanded = expanded
        self.__parent = None
        self.__children = []

    def __unicode__(self):
        return "%s[%s]" % (self.name, self.unlock_condition)

    def __str__(self):
        return "%s[%s]" % (self.name, self.unlock_condition)

    def __repr__(self):
        return "<Node: %s[%s]>" % (self.name, self.unlock_condition)

    @property
    def identifier(self):
        return self.__identifier

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        if value is not None:
            self.__parent = sanitize_string(value)

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value):
        if value is not None and isinstance(value, list):
            self.__children = value

    def update_children(self, identifier, mode=_ADD):
        """Updates the children with the given identifier and mode."""
        sane = sanitize_string(identifier)
        if mode is _ADD:
            if sane not in self.__children:
                self.__children.append(sane)
        elif mode is _DELETE:
            if sane in self.__children:
                self.__children.remove(sane)
        elif mode is _INSERT:
            self.__children = [sane]


class MultipleRootError(Exception):
    """Multiple Root problem in Tree."""
    pass


class Tree(object):
    """Tree of Nodes."""
    def __init__(self):
        """initializer."""
        self.nodes = {}
        self.root = None

    def add_node(self, node, parent=None):
        """Adds a Node to the Tree."""
        if parent is None:
            if self.root is not None:
                raise MultipleRootError
            else:
                self.root = node.identifier
        try:
            self.nodes[node.identifier]
        except KeyError:
            self.nodes.update({node.identifier: node})
        ret = self.__update_children(parent, node.identifier, _ADD)
#        print "add_node %s, %s" % (node.name, ret)
        node.parent = parent

    def create_node(self, name, unlock_condition, identifier=None, parent=None):
        """Create a child node for the node indicated by the 'parent' parameter"""
        node = Node(name, unlock_condition, identifier)
        self.add_node(node, parent)
        return node

    def expand_tree(self, nid=None, mode=_DEPTH, filter_fn=None):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        def real_true(pos):
            return True

        if nid is None:
            nid = self.root
        if filter_fn is None:
            filter_fn = real_true

        if filter_fn(nid):
            yield nid
            queue = self[nid].children
            while queue:
                if filter_fn(queue[0]):
                    yield queue[0]
                    expansion = self[queue[0]].children
                    if mode is _DEPTH:
                        queue = expansion + queue[1:]  # depth-first
                    elif mode is _WIDTH:
                        queue = queue[1:] + expansion  # width-first
                else:
                    queue = queue[1:]

    def get_node(self, nid):
        try:
            return self.nodes[nid]
        except KeyError:
            return None

    def is_branch(self, nid):
        """Return the following nodes of [nid]"""
        return self[nid].children

    def move_node(self, source, destination):
        """Move a node indicated by the 'source' parameter to the parent node
        indicated by the 'dest' parameter"""
        parent = self[source].parent
        self.__update_children(parent, source, _DELETE)
        self.__update_children(destination, source, _ADD)
        self.__update_parent(source, destination)

    def paste(self, nid, new_tree):
        """Paste a new tree to the original one by linking the root
of new tree to nid."""
        assert isinstance(new_tree, Tree)

        # check identifier replication

        if set(new_tree.nodes) & set(self.nodes):
            # error, duplicate node identifier
            # TODO: PEP8: deprecated form of raising exception
            raise ValueError, 'Duplicated nodes exists.'

        new_tree[new_tree.root].parent = nid
        self.__update_children(nid, new_tree.root, _ADD)
        self.nodes.update(new_tree.nodes)

    def remove_node(self, identifier):
        """Remove a node indicated by 'identifier'. All the successors are removed, too."""
        parent = self[identifier].parent
        remove = []  # temp. list for nodes which will be removed
        for id in self.expand_tree(identifier):
            # TODO: implementing this function as a recursive function:
            # check if node has children
            # true -> run remove_node with child_id
            # no -> delete node
            remove.append(id)

        for id in remove:
            del(self.nodes[id])

        self.__update_children(parent, identifier, _DELETE)

    def rsearch(self, nid, filter_fn=None):
        """Search the tree from nid to the root along links reversedly."""

        def real_true(p):
            return True

        if filter_fn is None:
            filter_fn = real_true
        current = nid
        while current is not None:
            if filter_fn(current):
                yield current
            current = self[current].parent

    def show(self, nid=None, level=_ROOT):
        """"Another implementation of printing tree using Stack
Print tree structure in hierarchy style.
For example:
Root
|___ C01
| |___ C11
| |___ C111
| |___ C112
|___ C02
|___ C03
| |___ C31
A more elegant way to achieve this function using Stack structure,
for constructing the Nodes Stack push and pop nodes with additional level info."""
        leading = ''
        lasting = '|___ '

        if nid is None:
            nid = self.root
        label = "{0}[{1}]".format(self[nid].name, self[nid].unlock_condition)

        queue = self[nid].children
        #print level
        if level == _ROOT:
            print(label)
        else:
            if level <= 1:
                leading += ('|' + ' ' * 4) * (level - 1)
            else:
                leading += ('|' + ' ' * 4) + (' ' * 5 * (level - 2))
            print("{0}{1}{2}".format(leading, lasting, label))

        if self[nid].expanded:
            level += 1
            for element in queue:
                self.show(element, level)  # recursive call

    def subtree(self, nid):
        """Return a COPY of subtree of the whole tree with the nid being the new root.
And the structure of the subtree is maintained from the old tree."""
        st = Tree()
        st.root = nid
        for node_n in self.expand_tree(nid):
            st.nodes.update({self[node_n].identifier: self[node_n]})
        return st

    def __contains__(self, identifier):
        return [node.identifier for node in self.nodes
                if node.identifier is identifier]

    def __getitem__(self, key):
        return self.nodes.get(key)

    def __len__(self):
        return len(self.nodes)

    def __setitem__(self, key, item):
        self.nodes.update({key: item})

    def __update_parent(self, nid, identifier):
        self[nid].parent = identifier

    def __update_children(self, nid, identifier, mode):
        if nid is None:
            return False
        else:
            if self[nid]:
                self[nid].update_children(identifier, mode)
                return True
            return False

    def __repr__(self):
        return "<Tree: %s>" % (self.root)


def build_nodes(class_type):
    """Builds nodes from all the Actions in the class_type, it should be LibraryAction,
    DesignerAction or Action."""
    # build nodes for all the actions in the grid.
    nodes = []
    for action in class_type.objects.all():
        try:
            if action.level and action.category:
#                print action.slug
                nodes.append(Node(action.slug, action.unlock_condition, action.slug))
        except AttributeError:
            nodes.append(Node(action.slug, action.unlock_condition, action.slug))
    return nodes


def build_trees(class_type):
    """Build the unlock_trees for the DesignerActions in the Grid."""
    nodes = build_nodes(class_type)
    trees = {}
    # loop through the nodes looking for possible root nodes. unlock_condition = True or False
    for node in nodes:
        if node.unlock_condition == "True" or node.unlock_condition == "False":
            t = Tree()
            t.create_node(node.name, node.unlock_condition, node.identifier)
            trees[node.name] = t

    for node in nodes:
        slugs = get_completed_action_slugs(node)
        for slug in slugs:
            for k in list(trees):
                if trees[k].get_node(slug):
                    trees[k].add_node(node, slug)
    # second pass because adding in the wrong order may cause problems
    for node in nodes:
        slugs = get_completed_action_slugs(node)
        for slug in slugs:
            for k in list(trees):
                if trees[k].get_node(slug):
                    trees[k].add_node(node, slug)
#                else:
#                    print "%s doesn't have %s in it." % (k, slug)
    return trees


def get_completed_action_slugs(node):
    ret = []
    l = node.unlock_condition.split('completed_action(')
    if len(l) > 1:
        index = l[1].find(')')
        ret.append(l[1][:index].strip('"\''))
        if len(l) > 2:
            index = l[1].find(')')
            ret.append(l[2][:index].strip('"\''))
    return ret


def get_actions_not_in_trees():
    """Returns the Action slug for actions that are not in any tree.  These actions are not
    reachable so they will not be unlocked."""
    ret = []
    nodes = build_nodes(DesignerAction)
    trees = build_trees(DesignerAction)
    # check all the nodes
    for node in nodes:
        in_tree = False
        for k in list(trees):
            tree = trees[k]
            if tree.get_node(node.identifier):
                in_tree = True
        if not in_tree:
            ret.append("%s: %s" % (node.identifier, node.unlock_condition))
    return ret
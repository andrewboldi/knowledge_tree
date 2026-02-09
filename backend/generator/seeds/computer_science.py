"""Computer Science seed definitions - fundamental concepts and theory.

This module contains formal definitions of foundational CS concepts,
from computational theory to data structures and algorithms.
Each definition includes:
- name: The canonical name of the concept
- definition_md: Formal definition in Markdown with LaTeX notation
- domain: Always "CS" for this module
- subfield: The CS subfield (e.g., "theory", "algorithms", "data_structures")
- complexity_level: 0 for fundamental concepts, higher for derived
- is_axiom: True for foundational definitions/axioms
- books: Reference texts where the concept is covered
- prerequisites: List of concept names that must be understood first
"""

CS_AXIOM_DEFINITIONS = [
    # ==========================================================================
    # COMPUTATIONAL THEORY - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Algorithm",
        "definition_md": """## Algorithm

An **algorithm** is a finite sequence of well-defined instructions for solving
a class of problems or performing a computation:

**Formal properties:**
1. **Finiteness:** Terminates after a finite number of steps
2. **Definiteness:** Each step is precisely defined
3. **Input:** Zero or more inputs from a specified set
4. **Output:** One or more outputs related to inputs
5. **Effectiveness:** Each step is basic enough to be carried out

**Representation:**
- Pseudocode
- Flowcharts
- Programming languages
- Mathematical notation

**Analysis dimensions:**
- **Correctness:** Does it produce the right output?
- **Time complexity:** How many operations?
- **Space complexity:** How much memory?

**Example (Euclidean algorithm for GCD):**
```
function gcd(a, b):
    while b ≠ 0:
        a, b = b, a mod b
    return a
```

**Church-Turing thesis:** Any effectively calculable function can be computed
by a Turing machine (algorithm).""",
        "domain": "CS",
        "subfield": "theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 1",
            "The Art of Computer Programming - Knuth, Vol. 1",
            "Algorithms - Sedgewick & Wayne, Ch. 1",
        ],
        "prerequisites": [],
    },
    {
        "name": "Turing Machine",
        "definition_md": """## Turing Machine

A **Turing machine** is an abstract model of computation that defines what it
means for a function to be computable:

**Formal definition:** A Turing machine is a 7-tuple:
$$M = (Q, \\Sigma, \\Gamma, \\delta, q_0, q_{accept}, q_{reject})$$

where:
- $Q$ = finite set of states
- $\\Sigma$ = input alphabet (not containing blank symbol $\\sqcup$)
- $\\Gamma$ = tape alphabet ($\\Sigma \\subseteq \\Gamma$, $\\sqcup \\in \\Gamma$)
- $\\delta: Q \\times \\Gamma \\to Q \\times \\Gamma \\times \\{L, R\\}$ = transition function
- $q_0 \\in Q$ = start state
- $q_{accept} \\in Q$ = accept state
- $q_{reject} \\in Q$ = reject state

**Components:**
- Infinite tape divided into cells
- Read/write head
- State register
- Transition table

**Configuration:** $(q, w, i)$ where $q$ = state, $w$ = tape contents, $i$ = head position

**Church-Turing thesis:** Turing machines capture the intuitive notion of
"computable." Any function computable by an algorithm is Turing-computable.

**Variants:** Multi-tape, nondeterministic, probabilistic (all equivalent in power).""",
        "domain": "CS",
        "subfield": "theory",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to the Theory of Computation - Sipser, Ch. 3",
            "Computational Complexity - Arora & Barak, Ch. 1",
        ],
        "prerequisites": ["Algorithm"],
    },
    {
        "name": "Computability",
        "definition_md": """## Computability

**Computability** is the study of which problems can be solved algorithmically:

**Decidable (recursive) language:**
A language $L$ is **decidable** if there exists a Turing machine $M$ that:
- Accepts all $w \\in L$
- Rejects all $w \\notin L$
- Always halts

**Recognizable (recursively enumerable) language:**
A language $L$ is **recognizable** if there exists a Turing machine that:
- Accepts all $w \\in L$
- May reject or loop forever for $w \\notin L$

**Undecidable problems:**

1. **Halting problem:** Given $\\langle M, w \\rangle$, does $M$ halt on input $w$?
   $$HALT = \\{\\langle M, w \\rangle : M \\text{ halts on } w\\}$$

2. **Post correspondence problem**

3. **Entscheidungsproblem:** Is a first-order logic statement provable?

**Hierarchy:**
$$\\text{Decidable} \\subsetneq \\text{Recognizable} \\subsetneq \\text{All languages}$$

**Rice's theorem:** Any non-trivial semantic property of Turing machines is undecidable.""",
        "domain": "CS",
        "subfield": "theory",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Introduction to the Theory of Computation - Sipser, Ch. 4-5",
            "Computability and Logic - Boolos et al.",
        ],
        "prerequisites": ["Turing Machine"],
    },
    # ==========================================================================
    # COMPLEXITY THEORY - Level 1
    # ==========================================================================
    {
        "name": "Big-O Notation",
        "definition_md": """## Big-O Notation

**Big-O notation** describes the asymptotic upper bound of a function's growth rate:

**Definition:** $f(n) = O(g(n))$ if there exist positive constants $c$ and $n_0$ such that:
$$0 \\leq f(n) \\leq c \\cdot g(n) \\quad \\forall n \\geq n_0$$

**Interpretation:** $f$ grows no faster than $g$ asymptotically.

**Related notations:**
- $\\Omega(g(n))$: Lower bound ($f(n) \\geq c \\cdot g(n)$)
- $\\Theta(g(n))$: Tight bound (both $O$ and $\\Omega$)
- $o(g(n))$: Strict upper bound ($\\lim_{n \\to \\infty} f(n)/g(n) = 0$)
- $\\omega(g(n))$: Strict lower bound

**Common complexity classes:**
| Notation | Name | Example |
|----------|------|---------|
| $O(1)$ | Constant | Array access |
| $O(\\log n)$ | Logarithmic | Binary search |
| $O(n)$ | Linear | Linear search |
| $O(n \\log n)$ | Linearithmic | Merge sort |
| $O(n^2)$ | Quadratic | Bubble sort |
| $O(2^n)$ | Exponential | Subset enumeration |

**Properties:**
- $O(f) + O(g) = O(\\max(f, g))$
- $O(f) \\cdot O(g) = O(f \\cdot g)$""",
        "domain": "CS",
        "subfield": "theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 3",
            "Algorithms - Sedgewick & Wayne, Ch. 1",
        ],
        "prerequisites": ["Algorithm"],
    },
    {
        "name": "P vs NP",
        "definition_md": """## P vs NP Problem

The **P vs NP problem** asks whether every problem whose solution can be quickly
verified can also be quickly solved:

**Class P (Polynomial time):**
$$P = \\{L : L \\text{ is decided by a deterministic TM in } O(n^k) \\text{ time}\\}$$

**Class NP (Nondeterministic Polynomial time):**
$$NP = \\{L : L \\text{ is decided by a nondeterministic TM in } O(n^k) \\text{ time}\\}$$

Equivalently: Problems with polynomial-time verifiable certificates.

**NP-Complete:**
A problem $L$ is NP-complete if:
1. $L \\in NP$
2. Every problem in NP reduces to $L$ in polynomial time

**Examples of NP-complete problems:**
- SAT (Boolean satisfiability)
- 3-SAT
- Traveling salesman (decision version)
- Graph coloring
- Subset sum

**The question:** Is $P = NP$ or $P \\neq NP$?

**Implications if $P = NP$:**
- Cryptography would be broken
- Many optimization problems become easy
- Mathematical proofs could be found automatically

**Millennium Prize Problem:** $1,000,000 for a proof either way.""",
        "domain": "CS",
        "subfield": "theory",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to the Theory of Computation - Sipser, Ch. 7",
            "Computational Complexity - Arora & Barak, Ch. 2",
            "Computers and Intractability - Garey & Johnson",
        ],
        "prerequisites": ["Big-O Notation", "Turing Machine"],
    },
    # ==========================================================================
    # DATA STRUCTURES - Level 0 (Foundational)
    # ==========================================================================
    {
        "name": "Data Structure",
        "definition_md": """## Data Structure

A **data structure** is a particular way of organizing and storing data to enable
efficient access and modification:

**Abstract Data Type (ADT):** Specification of behavior
- Defines operations and their semantics
- Independent of implementation

**Concrete implementation:** Actual organization in memory
- Determines time/space complexity of operations

**Fundamental categories:**

1. **Linear structures:**
   - Array, Linked List, Stack, Queue

2. **Trees:**
   - Binary Tree, BST, Heap, B-tree

3. **Graphs:**
   - Adjacency list, Adjacency matrix

4. **Hash-based:**
   - Hash table, Hash set

5. **Advanced:**
   - Trie, Segment tree, Union-Find

**Tradeoffs:**
| Operation | Array | Linked List | Hash Table | BST |
|-----------|-------|-------------|------------|-----|
| Access | $O(1)$ | $O(n)$ | $O(1)$ avg | $O(\\log n)$ |
| Search | $O(n)$ | $O(n)$ | $O(1)$ avg | $O(\\log n)$ |
| Insert | $O(n)$ | $O(1)$ | $O(1)$ avg | $O(\\log n)$ |
| Delete | $O(n)$ | $O(1)$ | $O(1)$ avg | $O(\\log n)$ |""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 0,
        "is_axiom": True,
        "books": [
            "Introduction to Algorithms - CLRS, Part III",
            "Data Structures and Algorithms - Aho, Hopcroft & Ullman",
        ],
        "prerequisites": ["Algorithm"],
    },
    {
        "name": "Array",
        "definition_md": """## Array

An **array** is a contiguous block of memory storing elements of the same type,
accessible by index:

**Definition:** A mapping from indices to elements:
$$A: \\{0, 1, ..., n-1\\} \\to T$$
where $T$ is the element type.

**Memory layout:**
$$\\text{address}(A[i]) = \\text{base} + i \\times \\text{sizeof}(T)$$

**Operations and complexity:**
| Operation | Complexity |
|-----------|------------|
| Access $A[i]$ | $O(1)$ |
| Search | $O(n)$ |
| Insert at end | $O(1)$ amortized |
| Insert at index | $O(n)$ |
| Delete | $O(n)$ |

**Types:**
- **Static array:** Fixed size at creation
- **Dynamic array:** Grows as needed (ArrayList, vector)
  - Doubling strategy: amortized $O(1)$ append

**Multi-dimensional arrays:**
$$A[i][j] = \\text{base} + (i \\times \\text{cols} + j) \\times \\text{sizeof}(T)$$

**Advantages:**
- Cache-friendly (spatial locality)
- Random access in $O(1)$
- Simple and memory-efficient

**Disadvantages:**
- Fixed size (static) or expensive resizing
- Expensive insertion/deletion in middle""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 10",
            "The Art of Computer Programming - Knuth, Vol. 1",
        ],
        "prerequisites": ["Data Structure"],
    },
    {
        "name": "Linked List",
        "definition_md": """## Linked List

A **linked list** is a linear data structure where elements are stored in nodes
connected by pointers:

**Node structure:**
```
class Node:
    data: T
    next: Node | null
```

**Types:**

1. **Singly linked list:**
   $$\\text{head} \\to [A|\\bullet] \\to [B|\\bullet] \\to [C|\\text{null}]$$

2. **Doubly linked list:**
   $$[\\text{null}|A|\\bullet] \\leftrightarrow [\\bullet|B|\\bullet] \\leftrightarrow [\\bullet|C|\\text{null}]$$

3. **Circular linked list:** Last node points to first

**Operations:**
| Operation | Singly | Doubly |
|-----------|--------|--------|
| Access by index | $O(n)$ | $O(n)$ |
| Insert at head | $O(1)$ | $O(1)$ |
| Insert at tail | $O(n)$ or $O(1)$* | $O(1)$ |
| Delete (given node) | $O(n)$ | $O(1)$ |
| Search | $O(n)$ | $O(n)$ |

*$O(1)$ if tail pointer maintained.

**Advantages:**
- Dynamic size
- Efficient insertion/deletion at known positions
- No wasted space

**Disadvantages:**
- No random access
- Extra memory for pointers
- Poor cache locality""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 10",
            "Data Structures and Algorithms - Aho, Hopcroft & Ullman",
        ],
        "prerequisites": ["Data Structure"],
    },
    {
        "name": "Stack",
        "definition_md": """## Stack

A **stack** is a Last-In-First-Out (LIFO) abstract data type:

**Operations:**
- $\\text{push}(x)$: Add element to top
- $\\text{pop}()$: Remove and return top element
- $\\text{peek}()$ / $\\text{top}()$: Return top element without removing
- $\\text{isEmpty}()$: Check if stack is empty

All operations are $O(1)$.

**Axioms (ADT specification):**
$$\\text{pop}(\\text{push}(S, x)) = (S, x)$$
$$\\text{top}(\\text{push}(S, x)) = x$$
$$\\text{isEmpty}(\\text{empty}) = \\text{true}$$
$$\\text{isEmpty}(\\text{push}(S, x)) = \\text{false}$$

**Implementations:**
- Array-based: Use index as stack pointer
- Linked list: Insert/delete at head

**Applications:**
- Function call stack (recursion)
- Expression evaluation and parsing
- Undo functionality
- Balanced parentheses checking
- DFS traversal

**Example - balanced parentheses:**
```
for char in expression:
    if char == '(':
        push(char)
    elif char == ')':
        if isEmpty(): return false
        pop()
return isEmpty()
```""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 10",
            "Data Structures and Algorithms - Aho, Hopcroft & Ullman",
        ],
        "prerequisites": ["Array", "Linked List"],
    },
    {
        "name": "Queue",
        "definition_md": """## Queue

A **queue** is a First-In-First-Out (FIFO) abstract data type:

**Operations:**
- $\\text{enqueue}(x)$: Add element to rear
- $\\text{dequeue}()$: Remove and return front element
- $\\text{front}()$ / $\\text{peek}()$: Return front element without removing
- $\\text{isEmpty}()$: Check if queue is empty

All operations are $O(1)$.

**Axioms (ADT specification):**
$$\\text{dequeue}(\\text{enqueue}(\\text{empty}, x)) = (\\text{empty}, x)$$
$$\\text{front}(\\text{enqueue}(\\text{empty}, x)) = x$$

**Implementations:**
- **Circular array:** Front and rear indices wrap around
- **Linked list:** Enqueue at tail, dequeue at head

**Variants:**
- **Deque (double-ended queue):** Insert/remove at both ends
- **Priority queue:** Dequeue by priority, not arrival order

**Applications:**
- BFS traversal
- Task scheduling
- Print queue
- Message buffering
- Simulation of waiting lines

**Circular array implementation:**
```
front = (front + 1) % capacity  // dequeue
rear = (rear + 1) % capacity    // enqueue
```""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 0,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 10",
            "Data Structures and Algorithms - Aho, Hopcroft & Ullman",
        ],
        "prerequisites": ["Array", "Linked List"],
    },
    # ==========================================================================
    # TREES AND GRAPHS - Level 1
    # ==========================================================================
    {
        "name": "Binary Tree",
        "definition_md": """## Binary Tree

A **binary tree** is a tree data structure where each node has at most two children:

**Recursive definition:**
A binary tree is either:
- Empty (null), or
- A node with data and two binary tree children (left, right)

**Node structure:**
```
class TreeNode:
    data: T
    left: TreeNode | null
    right: TreeNode | null
```

**Properties:**
- **Height:** Longest path from root to leaf
- **Depth:** Distance from root to node
- **Full binary tree:** Every node has 0 or 2 children
- **Complete binary tree:** All levels filled except possibly last (filled left-to-right)
- **Perfect binary tree:** All internal nodes have 2 children, all leaves at same level

**Node count bounds:**
- Minimum nodes at height $h$: $h + 1$
- Maximum nodes at height $h$: $2^{h+1} - 1$

**Traversals:**
- **In-order (LNR):** Left, Node, Right → sorted order for BST
- **Pre-order (NLR):** Node, Left, Right → copy tree
- **Post-order (LRN):** Left, Right, Node → delete tree
- **Level-order:** BFS, level by level

**Applications:** Expression trees, BST, heaps, decision trees.""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 12",
            "Data Structures and Algorithms - Aho, Hopcroft & Ullman",
        ],
        "prerequisites": ["Data Structure"],
    },
    {
        "name": "Binary Search Tree",
        "definition_md": """## Binary Search Tree (BST)

A **Binary Search Tree** is a binary tree satisfying the BST property:

**BST Property:** For every node $x$:
- All keys in left subtree $< x.\\text{key}$
- All keys in right subtree $> x.\\text{key}$

**Operations (average case, balanced):**
| Operation | Complexity |
|-----------|------------|
| Search | $O(\\log n)$ |
| Insert | $O(\\log n)$ |
| Delete | $O(\\log n)$ |
| Min/Max | $O(\\log n)$ |

**Worst case:** $O(n)$ when tree degenerates to linked list.

**Search algorithm:**
```
function search(node, key):
    if node == null or node.key == key:
        return node
    if key < node.key:
        return search(node.left, key)
    else:
        return search(node.right, key)
```

**In-order traversal** yields sorted order.

**Balanced variants:**
- **AVL tree:** Height-balanced (heights differ by at most 1)
- **Red-Black tree:** Color-balanced, used in many libraries
- **B-tree:** Multi-way, used in databases

**Applications:** Sorted data storage, range queries, ordered maps/sets.""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 12-13",
            "Algorithms - Sedgewick & Wayne, Ch. 3",
        ],
        "prerequisites": ["Binary Tree"],
    },
    {
        "name": "Graph",
        "definition_md": """## Graph

A **graph** is a structure consisting of vertices connected by edges:

**Formal definition:**
$$G = (V, E)$$
where $V$ is the set of vertices and $E \\subseteq V \\times V$ is the set of edges.

**Types:**
- **Directed (digraph):** Edges have direction $(u, v) \\neq (v, u)$
- **Undirected:** Edges are unordered pairs $\\{u, v\\}$
- **Weighted:** Edges have associated weights $w: E \\to \\mathbb{R}$
- **Connected:** Path exists between every pair of vertices
- **Acyclic:** Contains no cycles (DAG if directed)

**Representations:**
1. **Adjacency matrix:** $A[i][j] = 1$ if edge $(i,j)$ exists
   - Space: $O(|V|^2)$
   - Edge check: $O(1)$

2. **Adjacency list:** List of neighbors for each vertex
   - Space: $O(|V| + |E|)$
   - Edge check: $O(\\text{degree})$

**Key properties:**
- $|E| \\leq |V|^2$ (directed) or $|V|(|V|-1)/2$ (undirected)
- Sum of degrees $= 2|E|$

**Traversals:**
- **BFS:** Level-order, shortest paths in unweighted graphs
- **DFS:** Explore deeply first, topological sort, cycle detection

**Applications:** Social networks, maps, dependencies, state machines.""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 22",
            "Algorithms - Sedgewick & Wayne, Ch. 4",
        ],
        "prerequisites": ["Data Structure"],
    },
    {
        "name": "Hash Table",
        "definition_md": """## Hash Table

A **hash table** is a data structure that maps keys to values using a hash function:

**Components:**
1. **Array** of buckets/slots
2. **Hash function** $h: K \\to \\{0, 1, ..., m-1\\}$

**Ideal operation complexities:**
| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | $O(1)$ | $O(n)$ |
| Search | $O(1)$ | $O(n)$ |
| Delete | $O(1)$ | $O(n)$ |

**Hash function properties:**
- Deterministic
- Uniform distribution
- Fast to compute

**Collision resolution:**

1. **Chaining:** Each bucket contains a linked list
   - Load factor $\\alpha = n/m$
   - Expected chain length $= \\alpha$

2. **Open addressing:** Find next empty slot
   - Linear probing: $h(k, i) = (h(k) + i) \\mod m$
   - Quadratic probing: $h(k, i) = (h(k) + c_1 i + c_2 i^2) \\mod m$
   - Double hashing: $h(k, i) = (h_1(k) + i \\cdot h_2(k)) \\mod m$

**Load factor:** $\\alpha = n/m$ where $n$ = elements, $m$ = table size.
Resize when $\\alpha$ exceeds threshold (typically 0.75).

**Applications:** Dictionaries, caches, sets, database indexing.""",
        "domain": "CS",
        "subfield": "data_structures",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 11",
            "Algorithms - Sedgewick & Wayne, Ch. 3",
        ],
        "prerequisites": ["Array"],
    },
    # ==========================================================================
    # ALGORITHMS - Level 1
    # ==========================================================================
    {
        "name": "Sorting Algorithm",
        "definition_md": """## Sorting Algorithm

A **sorting algorithm** rearranges elements of a sequence into a specified order:

**Problem:** Given array $A[1..n]$, produce permutation $A'$ such that:
$$A'[1] \\leq A'[2] \\leq ... \\leq A'[n]$$

**Comparison-based sorts:**
| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes |
| Insertion sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes |
| Merge sort | $O(n\\log n)$ | $O(n\\log n)$ | $O(n\\log n)$ | $O(n)$ | Yes |
| Quick sort | $O(n\\log n)$ | $O(n\\log n)$ | $O(n^2)$ | $O(\\log n)$ | No |
| Heap sort | $O(n\\log n)$ | $O(n\\log n)$ | $O(n\\log n)$ | $O(1)$ | No |

**Lower bound:** Comparison-based sorting requires $\\Omega(n \\log n)$ comparisons.
$$\\log_2(n!) = \\Theta(n \\log n)$$

**Non-comparison sorts:**
- Counting sort: $O(n + k)$ where $k$ = range
- Radix sort: $O(d(n + k))$ where $d$ = digits
- Bucket sort: $O(n)$ average

**Stability:** Stable sort preserves relative order of equal elements.

**In-place:** Uses $O(1)$ extra memory.""",
        "domain": "CS",
        "subfield": "algorithms",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 2, 6-8",
            "Algorithms - Sedgewick & Wayne, Ch. 2",
        ],
        "prerequisites": ["Algorithm", "Array", "Big-O Notation"],
    },
    {
        "name": "Recursion",
        "definition_md": """## Recursion

**Recursion** is a method where the solution to a problem depends on solutions
to smaller instances of the same problem:

**Components:**
1. **Base case:** Condition that stops recursion
2. **Recursive case:** Problem decomposition and recursive call

**Example - Factorial:**
$$n! = \\begin{cases} 1 & \\text{if } n = 0 \\\\ n \\cdot (n-1)! & \\text{if } n > 0 \\end{cases}$$

```python
def factorial(n):
    if n == 0:          # base case
        return 1
    return n * factorial(n - 1)  # recursive case
```

**Recurrence relations:** Mathematical form of recursive algorithms
$$T(n) = aT(n/b) + f(n)$$

**Master theorem:** Solves recurrences of above form:
- If $f(n) = O(n^{\\log_b a - \\epsilon})$: $T(n) = \\Theta(n^{\\log_b a})$
- If $f(n) = \\Theta(n^{\\log_b a})$: $T(n) = \\Theta(n^{\\log_b a} \\log n)$
- If $f(n) = \\Omega(n^{\\log_b a + \\epsilon})$: $T(n) = \\Theta(f(n))$

**Tail recursion:** Recursive call is last operation; can be optimized to iteration.

**Stack overflow:** Too many recursive calls exhaust stack space.

**Applications:** Tree traversal, divide-and-conquer, dynamic programming.""",
        "domain": "CS",
        "subfield": "algorithms",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 4",
            "Structure and Interpretation of Computer Programs - Abelson & Sussman",
        ],
        "prerequisites": ["Algorithm", "Stack"],
    },
    {
        "name": "Dynamic Programming",
        "definition_md": """## Dynamic Programming

**Dynamic programming (DP)** solves problems by breaking them into overlapping
subproblems and storing their solutions:

**Key properties:**
1. **Optimal substructure:** Optimal solution contains optimal solutions to subproblems
2. **Overlapping subproblems:** Same subproblems are solved multiple times

**Approaches:**
1. **Top-down (memoization):** Recursive with caching
2. **Bottom-up (tabulation):** Iterative, building up from base cases

**Example - Fibonacci:**
$$F(n) = F(n-1) + F(n-2), \\quad F(0) = 0, F(1) = 1$$

Naive recursive: $O(2^n)$
DP (memoization or tabulation): $O(n)$

**Classic DP problems:**
- Longest Common Subsequence: $O(mn)$
- Knapsack: $O(nW)$
- Edit Distance: $O(mn)$
- Matrix Chain Multiplication: $O(n^3)$
- Shortest paths (Floyd-Warshall): $O(n^3)$

**State definition:** The key insight is defining what constitutes a "subproblem"
$$dp[i][j] = \\text{value for subproblem involving indices } i, j$$

**Recurrence:** Express $dp[i][j]$ in terms of smaller subproblems.

**Space optimization:** Often can reduce from $O(n^2)$ to $O(n)$ by only keeping
previous row/column.""",
        "domain": "CS",
        "subfield": "algorithms",
        "complexity_level": 1,
        "is_axiom": False,
        "books": [
            "Introduction to Algorithms - CLRS, Ch. 15",
            "Algorithms - Sedgewick & Wayne, Ch. 5",
        ],
        "prerequisites": ["Recursion", "Big-O Notation"],
    },
]

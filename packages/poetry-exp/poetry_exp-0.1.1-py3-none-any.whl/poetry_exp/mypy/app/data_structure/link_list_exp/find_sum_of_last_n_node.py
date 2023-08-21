"""


Method 5 (Use of two pointers requires single traversal)
Maintain two pointers reference pointer and main pointer.
Initialize both reference and main pointers to head.
First move reference pointer to n nodes from head and while traversing accumulate nodes data to some variable, say sum.
Now move both pointers simultaneously until reference pointer reaches to the end of the list and
while traversing accumulate all nodes data to sum pointed by the reference pointer
and accumulate all nodes data to some variable, say temp, pointed by the main pointer.
Now, (sum-temp) is the required sum of the last n nodes.


// utility function to find the sum of last 'n' nodes
int sumOfLastN_NodesUtil(struct Node* head, int n)
{
    // if n == 0
    if (n <= 0)
        return 0;

    int sum = 0, temp = 0;
    struct Node* ref_ptr, *main_ptr;
    ref_ptr = main_ptr = head;

    // traverse 1st 'n' nodes through 'ref_ptr' and
    // accumulate all node's data to 'sum'
    while (ref_ptr != NULL && & n--) {
        sum += ref_ptr->data;

        // move to next node
        ref_ptr = ref_ptr->next;
    }

    // traverse to the end of the linked list
    while (ref_ptr != NULL) {

        // accumulate all node's data to 'temp' pointed
        // by the 'main_ptr'
        temp += main_ptr->data;

        // accumulate all node's data to 'sum' pointed by
        // the 'ref_ptr'
        sum += ref_ptr->data;

        // move both the pointers to their respective
        // next nodes
        main_ptr = main_ptr->next;
        ref_ptr = ref_ptr->next;
    }

    // required sum
    return (sum - temp);
}

"""
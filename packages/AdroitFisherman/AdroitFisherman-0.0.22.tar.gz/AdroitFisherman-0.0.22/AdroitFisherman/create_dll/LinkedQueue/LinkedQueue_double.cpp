#include "DataStorage.h"
#include <iostream>
#include "LinkedQueue_double.h"
DataStorage::LinkedQueue<double>QUEUE = DataStorage::LinkedQueue<double>();
bool init_queue()
{
	bool tag = QUEUE.InitQueue();
	return tag;
}
void destroy_queue()
{
	QUEUE.DestroyQueue();
}
void clear_queue()
{
	QUEUE.ClearQueue();
}
bool queue_empty()
{
	bool tag = QUEUE.QueueEmpty();
	return tag;
}
int queue_length()
{
	return QUEUE.QueueLength();
}
double get_head()
{
	return QUEUE.GetHead();
}
bool en_queue(double elem)
{
	bool tag = QUEUE.EnQueue(elem);
	return tag;
}
double de_queue()
{
	return QUEUE.DeQueue();
}
void queue_traverse()
{
	QUEUE.QueueTraverse();
}
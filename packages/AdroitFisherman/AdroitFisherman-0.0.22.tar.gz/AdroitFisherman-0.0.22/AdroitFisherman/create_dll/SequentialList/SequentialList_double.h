#ifndef SEQUENTIALLIST_DOUBLE
#define SEQUENTIALLIST_DOUBLE
#include "framework.h"
#include "DataStorage.h"
#include <iostream>
extern "C" __declspec(dllimport) void set_capacity(int maxsize);
extern "C" __declspec(dllimport) bool init_list();
extern "C" __declspec(dllimport) void destroy_list();
extern "C" __declspec(dllimport) void clear_list();
extern "C" __declspec(dllimport) bool list_empty();
extern "C" __declspec(dllimport) int list_length();
extern "C" __declspec(dllimport) double get_elem(int index);
extern "C" __declspec(dllimport) int locate_elem(double elem);
extern "C" __declspec(dllimport) double prior_elem(double elem);
extern "C" __declspec(dllimport) double next_elem(double elem);
extern "C" __declspec(dllimport) bool list_insert(int index, double elem);
extern "C" __declspec(dllimport) bool list_delete(int index);
extern "C" __declspec(dllimport) void traverse_list();
#endif // !SEQUENTIALLIST_DOUBLE

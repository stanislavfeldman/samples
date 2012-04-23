#include <iostream>
#include "LinkedList.hpp"
#include "Time.hpp"

using namespace std;

int main()
{
	double start_time = Time::get_current_time();
	LinkedList<int> list = LinkedList<int>();
	list.append(1);
	list.append(2);
	list.append(3);
	//list.insert(1, 555);
	cout << list.get(1) << endl;
	cout << list.get() << endl;
	list.print();
	cout << list.pop() << endl;
	list.print();
	cout << "prog duration: " << Time::get_current_time() - start_time << " ms" << endl;
	return 0;
}

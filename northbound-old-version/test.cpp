#include <iostream>
#include <iterator>
#include <vector>

using namespace std;

int main() {
	vector<int> vec;

	istream_iterator<int> cin_it(cin);
	istream_iterator<int> eof;

	while ( cin_it != eof ) {
		vec.push_back( *cin_it++ );
	}

	for( int i = 0; i < vec.size(); i++ ){
		cout << vec[i] << endl;
	}
}
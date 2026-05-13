NAME := "pynef-c-binds"

$(NAME):
	gcc -fPIC -c -I/usr/include/python3.11 -Wall -lpython3.11 -ldl c_binds/c_binds.c -o bin/pynef_cbinds.o 
	gcc -shared bin/pynef_cbinds.o -o bin/pynef_cbinds.so

example:
	gcc -I/usr/include/python3.11 -Wall -lpython3.11 bin/pynef_cbinds.so c_example.c -o bin/c_example

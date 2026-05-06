NAME := "pynef-c-binds"

$(NAME):
	gcc -fPIC -c -I/usr/include/python3.14 -fno-strict-overflow -Wsign-compare -march=x86-64 -mtune=generic -O3 -pipe -fno-plt -fexceptions -Wp,-D_FORTIFY_SOURCE=3 -Wformat -Werror=format-security -fstack-clash-protection -fcf-protection -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer -ffile-prefix-map=/build/python/src=/usr/src/debug/python -flto=auto -ffat-lto-objects -DNDEBUG -Wall -lpython3.14 -ldl c_binds/c_binds.c -o bin/pynef_cbinds.o 
	gcc -shared bin/pynef_cbinds.o -o bin/pynef_cbinds.so

example: $(NAME)
	gcc c_example.c bin/pynef_cbinds.so

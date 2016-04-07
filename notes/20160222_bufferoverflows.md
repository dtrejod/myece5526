Devin Trejo
Notes for Computer Intrusion 20160222

In C we refer to function calls as a stack. The bottom of the stack has
larger address while the top of the stack has smaller addresses. A stack
pointer keeps track of where you currently are in the stack.

There are two functions that are used to manipulate a stack. 'pop' and 
'push' where pop takes things off the stack while push puts things on to
the stack. 

```
--------------------- Smaller Memory Address
-                   -
-                   -
-                   -
-                   -
-                   -
-                   -
-                   - <- Stack Pointer
  -- Return Value --
-                   - 
-                   -
-                   -
-                   -
-       Main()      -
--------------------- Larger Memory Address

|

--------------------- Smaller Memory Address
-                   -
 -- Return Value1 --     <- Stack Pointer
-                   - }
-                   - } My Function 
-                   - }
-                   - }
-                   - 
 -- Return Value0 --     <- Frame Pointer
-                   - 
-                   -
-                   -
-                   -
-       Main()      -
--------------------- Larger Memory Address
```

Adversary Model. This model doesn't have physical access to the server but 
it can send data to the server. 

Web-servers process requests received by a client. We worry about 
1. confidentiality, 
2. authenticity, 
3. availability.

Mat Honan, a writer for Wired.com, had three accounts: one at gmail, one 
on Apple (@me.com), and an Amazon accont. The recovery process for gmail
was to have a backup email address to where it would send a recover message
to. The recovery process for Apple's @me.com you would reset your password
by using the last 4 digits our your credit card. Amazon allowed you to add
a credit card to an account without logging in by just knowing their email.
To do an Amazon password reset you need to know one of the credit numbers. 
<Source: http://www.wired.com/2012/08/apple-amazon-mat-honan-hacking/>


Buffer Overflows:

``` C
# c program
#
# filename: readreq.c
#
# include <stdio.h>
int read_req(void){
    char buf[128];
    int i;
    gets(buf);
    
    // Convert to string to int
    //
    i = atoi(buf);
    return i;
}

int main (int ac, char **arg){
    int x = read_req();
    printf("x=%d\n",x);
}
```

Compile command:

``` shell
$ gcc -g readreq.c -o readreq.exe
```

Run the debugger:

``` shell
$ gdb readreq
(gdb) info reg  # Prints the register
(gdb) b read_req # put breakpoint in read_req fuction
(gdb) r # run the function
(gdb) info reg
esp = stack pointer
ebp = frame pointer
eip = Instruction Pointer
(gdb) disass read_req # We are disassembly the function read_request
                      # Shows the raw assembly code
(gdb) print &buff[0] # Show address for the location of this variable in 
                     # memory
(gdb) x $ebp # Show location of frame pointer
(gdb) next # Run the next instruction. 
````

Looking at the raw memory locations using the debuger a user can manipulate
the values stored at important locations in memory. For example, with the
gets command we see that there is no limitation to the length of a user 
input. This allows for a hacker to craft a input in the program that will
overwrite the stack/frame pointer memory value. 

How do we avoid buffer overflows?
1. Use functions that boundary checks. Avoid buggy functions like 'gets()' 
and use function 'fgets()'. Don't avoid compiler warnings. 
2. Use tools to find bugs. "Static Analysis" = static because you are not
running the code the static analysis itselfs will look at your code and 
determine if any of it is problematic. 
3. Use memory safe languages. Use Python, Java, C#. 

Stack Canary
A stack canary places a buffer between your memory allocations and your 
return pointers. Issues also occur if a hacker knows the contents of a 
canary beforehand. Before a return statement is execute the return call 
will check to see if the canary has been overwritten. 

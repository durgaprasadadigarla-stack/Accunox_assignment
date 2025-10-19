Problem statement-3:

Explaining the code snippet:

package main

import "fmt"

func main() {

> **cnp** **:=** **make(chan** **func(),** **10)** **for** **i** **:=**
> **0;** **i** **\<** **4;** **i++** **{**
>
> **go** **func()** **{**
>
> **for** **f** **:=** **range** **cnp** **{** **f()**
>
> **}** **}()**
>
> **}**
>
> **cnp** **\<-** **func()** **{** **fmt.Println("HERE1")**
>
> **}** fmt.Println("Hello")

}

The following code attempts to create 4 go routines waiting for a
function to execute.

Package main:

> ● Used to declare that the program belongs to the main package.
>
> ● By declaring package main the compiler recognises it as an
> executable program ● The execution of the program start from package
> main

Import fmt:

> ● This line imports go’s standard library format package.
>
> ● This package is used to print the text. For example,
> fmt.println(“HELLO”)

func main():

> ● This line defines the main function.
>
> ● The program always starts running from the main function.

cnp := make(chan func(),10)

> ● This line creates a channel named cnp that can hold up to 10
> functions. ● The functions are stored in queue format in the channel.

for i := 0; i \< 4; i++ {

> go func() {
>
> for f := range cnp {
>
> f()
>
> ● It runs the inner block 4times, which means we are going to start 4
> go routines.
>
> ● go fun() defines an anonymous function and immediately runs it in
> the background. ● The 4 go routines which are created runs this
> function concurrently.
>
> ● for f := range cnp waits for a function to arrive in the channel. ●
> f() calls the function,executing whatever is inside it.

cnp \<- func() {

> fmt.Println("HERE1")
>
> ● func() defines an anonymous function and inside the function
> fmt.Println( “HERE 1”) prints HERE1 when the function is run.
>
> ● cnp\<- sends the function into the channel.

fmt.Println("Hello")

> ● This line prints “Hello” to the console.

Why here1 is not getting printed ?

> ● The go routines we create in the program runs in the background.
>
> ● In this program the main functions exits before any of the four go
> routines execute the function we pass into the channel so this program
> can't print here1.
>
> ● Since the execution of the prohram stops immediately after exiting
> the main function.

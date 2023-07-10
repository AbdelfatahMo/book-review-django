// Declare numbers
var y = 0;
// Declare strings
let str = 'my name is Great'
// for loop as java
for (i = 10.0; i >= -10; i--) {
    console.log(y += i + .5)
}
// Array
myThings = [1, 2, 3, 4, 5, 6, 'ds', 'fdsf']
// Append new 
myThings.push(20)
myThings.forEach(element => {
    console.log(element)
});

// Dictionary
dict = { no1: 1, no2: myThings }
console.log(dict.no2)

// Function
function myFunc(a, b, c) {
    if (a + b < c) {
        return c;
    } else if (a - c < b) {
        return b;
    } else {
        return a + b + c;
    }
}
console.log(myFunc(1, 2, 3))

// Classes
class Adder {
    constructor(toAdd) {
        this.toAdd = toAdd;
    }
    add(n) {
        return this.toAdd + n;
    }
}

a = new Adder(10)
console.log(a.add(10.175))

// Arrow Functions
const o1 = {
    outer: function () {
        console.log(this);// "this" refers to o1
        const inner = function () {
            console.log(this);// "this" refers to the "window"
        }
        inner();
    }
}
// Defining the inner function using arrow synta
const o2 = {
    outer: function () {
        console.log(this);
        // refers to o2
        const inner = () => {
            console.log(this);
        }
        inner()
    }
}

const numbers = [1, 2, 3, 4, 5]
const doubled = numbers.map((n) => { return n * 2 });
console.log(doubled)
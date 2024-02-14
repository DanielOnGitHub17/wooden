// math
let randInt = (x, y) => parseInt((y-x+1)*Math.random() + x)
, choice = (array) => array[randInt(0, array.length)] 
, near = (x, y) => Math.abs(x-y) < 0.00001;

// DOM
let get = (id) => document.getElementById(id)
  , getS = (query) => document.querySelector(query)
  , getAll = (query) => document.querySelectorAll(query)
  , make = (tag='div') => document.createElement(tag)
  , add = (element, to=document.body) => to.appendChild(element);

// misc

let copy = (array) => JSON.parse(JSON.stringify(array)) 
, logTurn = (obj) => (console.log(obj), obj)
, transfer = (object, from, to) => to.push(from.splice(from.indexOf(object), 1)[0]);

//   h.ondragstart = ()=>{
//     h.x = event.screenX;
//     h.y = event.screenY;
// }
// ()=>{
//     h.x = event.screenX;
//     h.y = event.screenY;
// }
// h.ondrag = ()=>{
//     h.style.left = (event.screenX-h.x)+"px";
//     h.style.top = (event.screenY-h.y)+"px";
// }
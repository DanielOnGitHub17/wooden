// math
let randInt = (x, y) => parseInt((y-x+1)*Math.random() + x);

let get = (id) => document.getElementById(id)
  , getS = (query) => document.querySelector(query)
  , getAll = (query) => document.querySelectorAll(query)
  , make = (tag='div') => document.createElement(tag)
  , add = (element, to=document.body) => to.appendChild(element);

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
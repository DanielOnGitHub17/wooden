// math
let randInt = (x, y) => parseInt((y-x+1)*Math.random() + x);

let get = (id) => document.getElementById(id)
  , getS = (query) => document.querySelector(query)
  , getAll = (query) => document.querySelectorAll(query)
  , make = (tag='div') => document.createElement(tag)
  , add = (element, to=document.body) => to.appendChild(element);
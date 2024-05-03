const combinations = {
    "enter": "enter",
    "backspace": "backspace",
    "tab": "tab",
    "left": "left",
    "up": "up",
    "down": "down",
    "right": "right",
    "F11": "f11",
    "ALT F4": "alt+f4", 
    "Min Window": "win+down",
    "Max Window": "win+up",
    "Restore Window": "win+shift+up",
    "lang": "alt+shift",
    "c": "c",
    "f": "f",
    //lbv_o
    "m": "m"
}

const comb_wrapper = document.querySelector('div.combinations')
for (const combination in combinations) comb_wrapper.innerHTML += `<div class="item btn" combination="${combinations[combination]}">${combination}</div>`


fetch('/deviceName').then(r => r.json()).then(r => document.querySelector('div.device-name').innerText = r)


const buttons = document.querySelectorAll('div.btn[combination]')
buttons.forEach(el => el.addEventListener('click', e => fetch(getParams('/keyboard', {key: el.getAttribute('combination')}))))


const touchscreen = document.querySelector('div.touch-screen')
let increment = 0
let req = 0

let last_x
let last_y

touchscreen.addEventListener('touchstart', e => {
    last_x = e.touches[0].clientX
    last_y = e.touches[0].clientY
    touchscreen.style.backgroundColor = '#ffffff0a'
})

touchscreen.addEventListener('touchmove', e => {
    increment += 1
    req += 1
    power = 1.5 // менять для регулировки чуствительности
    if (req == 3){

        delta_x = e.touches[0].clientX - last_x
        delta_y = e.touches[0].clientY - last_y

        fetch(getParams('/mouseMove', {x: delta_x*power, y: delta_y*power }))

        req = 0

        last_x = e.touches[0].clientX
        last_y = e.touches[0].clientY
    }
})


touchscreen.addEventListener('touchend', e => {
    touchscreen.style.backgroundColor = '#070707'
    if (increment == 0) fetch('/mouseClick')
    increment = 0
})


document.getElementById("input-keyboard").focus();
const audio_svg = document.getElementById('change-svg');

window.onscroll = (e) => {
    e.preventDefault()
  };

function changeImage(){
    if (audio_svg.attributes.src.value == 'assets/working-audio.svg'){
        audio_svg.attributes.src.value = 'assets/blocked-audio.svg';
    } else {
        audio_svg.attributes.src.value = 'assets/working-audio.svg';
    }
};
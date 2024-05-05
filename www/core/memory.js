class Memory {
    constructor (path = 'memory') {
        this.path = path
    }
    get (name) {
        return localStorage.getItem(this.path + '.' + name)
    }
    set (name, value) {
        localStorage.setItem(this.path + '.' + name, value)
    }
}

function get_params(params = {}){
    return Object.keys(params).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(params[key])).join('&');
}
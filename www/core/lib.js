const len = (obj) => {return obj.length};
const getParams = (path = null, params) => {
    str = []
    for (const param in params) {
        str.push(`${encodeURIComponent(param)}=${encodeURIComponent(params[param])}`) 
    }
    str = str.join('&')
    return path == null ? str : path + '?' + str
}
function strToInt(el) {
    const v = Number(el?.value);
    return Number.isInteger(v) ? v : NaN;
}

function strToFloat(el) {
    const v = Number(el?.value);
    return isNaN(v) ? NaN : v;
}

function showFieldError(id, msg) {
    alert(msg);
    const el = document.getElementById(id);
    if (el) { el.focus(); el.select(); }
}

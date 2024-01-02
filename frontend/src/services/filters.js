export function money(value) {
    if (typeof value !== "number") {
        return value;
    }
    let formatter = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
    return formatter.format(value);
}

export function date(value) {
    if (!value) return "";
    let dateObj = new Date(value);
    let day = ("0" + dateObj.getDate()).slice(-2);
    let month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
    let year = dateObj.getFullYear();
    return `${day}/${month}/${year}`;
}
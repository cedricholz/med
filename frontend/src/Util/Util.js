export const getCurrencyStringFromNumber = (
    amount,
    removeTrailingZeros = false
) => {
    const currencyFormatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    })
    let formattedAmount = currencyFormatter.format(amount)

    if (removeTrailingZeros && formattedAmount.endsWith(".00")) {
        formattedAmount = formattedAmount.substring(0, formattedAmount.length - 3)
    }

    return formattedAmount
}

export const numberWithCommas = (number) => {
    if (!number) {
        return number
    }
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}


export const createFilePreview = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(file)
    })
}

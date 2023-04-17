function onScanSuccess(decodedText, decodedResult) {
    window.location.href = `/search?ean=${decodedText}`
}

function onScanFailure(error) {
    console.warn(`Code scan error = ${error}`)
}

let html5QrcodeScanner = new Html5QrcodeScanner('qr-reader', {
    fps: 10,
    qrbox: { width: 220, height: 100 },
})
html5QrcodeScanner.render(onScanSuccess, onScanFailure)

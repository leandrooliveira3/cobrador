function copiarTexto() {
    const textoResumo = document.getElementById('texto-resumo');
    if (!textoResumo) return;
    
    // Extrai o texto limpo, sem tags HTML, mantendo os separadores |
    let textToCopy = textoResumo.innerText;
    textToCopy = textToCopy.replace(/\n/g, ' ').trim();

    navigator.clipboard.writeText(textToCopy).then(() => {
        const toastEl = document.getElementById('copyToast');
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }).catch(err => {
        console.error('Erro ao copiar texto: ', err);
    });
}

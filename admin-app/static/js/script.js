document.addEventListener('DOMContentLoaded', function() {
    // Beispiel: API-Schlüssel aus dem Local Storage holen und entschlüsseln (Platzhalter)
    let apiKey = localStorage.getItem('api_key');
    if (apiKey) {
        // Entschlüsselungslogik hier einfügen
        console.log('API-Schlüssel geladen:', apiKey);
    } else {
        console.log('Kein API-Schlüssel gefunden');
    }
});
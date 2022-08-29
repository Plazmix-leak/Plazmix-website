const API_ENDPOINT = 'https://api.plazmix.net'
const API_LOCAL_ENDPOINT = 'https://ap.plazmix.net/api'


function caseNum(titles) {
    const cases = [2, 0, 1, 1, 1, 2];
    return function (number) {
        number = Math.abs(number);
        let c =
            (number % 100 > 4 && number % 100 < 20) ? 2 :
                cases[(number % 10 < 5) ? number % 10 : 5];
        return titles[c];
    }
}
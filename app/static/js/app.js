(() =>{

    const $doc = document;
    const $time = $doc.getElementsByClassName('topics-time');
    const $new = $doc.getElementsByClassName('topics-label');
    const topicsLen = $time.length;
    let newDate = new Date();
    newDate.setDate(newDate.getDate() - 7);
    let yyyy = String(newDate.getFullYear());
    let mm = newDate.getMonth() + 1;
    mm = ('0' + mm).slice(-2);
    let dd = newDate.getDate();
    dd = ('0' + dd).slice(-2);
    newDate = yyyy + mm + dd;

    // function AutoLink(str) {
    //     var regexp_url = /((h?)(ttps?:\/\/[a-zA-Z0-9.\-_@:/~?%&;=+#',()*!]+))/g; // ']))/;
    //     var regexp_makeLink = function(all, url, h, href) {
    //         return '<a href="h' + href + '">' + url + '</a>';
    //     }
    //     return str.replace(regexp_url, regexp_makeLink);
    // }

    const init = () => {
        let index = 0;
        while(index < topicsLen){
            if ($time[index].getAttribute('datetime') > newDate){
                $new[index].style.display = 'inline-block';
                $new[index].style.whitespace = 'nowrap';
            } else {
                $new[index].style.display = 'none';
            }
            index++;
        };
        // index = 0;
        // while(index < $doc.getElementsByClassName('js-autolink').length) {
        //     $doc.getElementsByClassName('js-autolink')[index].innerText = AutoLink($doc.getElementsByClassName('js-autolink')[index].innerText);
        //     index++;
        // }
    };
    init();

})();


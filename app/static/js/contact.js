(() =>{

    const $doc = document;
    const $option = $doc.getElementsByTagName('option');
    const $violation = $doc.getElementsByClassName('violation')
    const $requiredViolation = $doc.getElementsByClassName('required-violation')

    //お問い合わせ確認
    const contactClick = (e) => {
        // e.preventDefault();
        let index = 0;
        while(index < $violation.length){
            $violation[index].style.display = 'none';
            index++;
        };
        let violation = 0;
        index = 0;
        while(index < $doc.getElementsByClassName('required-field').length){
            if($doc.getElementsByClassName('required-field')[index].value == "") {
                $requiredViolation[index].style.display = 'block';
                violation++;
            }
            index++;
        };
        let regex = /^0\d{1,3}-?\d{2,4}-?\d{3,4}$/;
        if(!($doc.getElementById('tel').value == "") && regex.test($doc.getElementById('tel').value) == false) {
            $doc.getElementById('tel-format').style.display = 'block';
            violation++;
        };
        regex = /^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]+.[A-Za-z0-9]+$/;
        if(!($doc.getElementById('email').value == "") && regex.test($doc.getElementById('email').value) == false) {
            $doc.getElementById('email-format').style.display = 'block';
            violation++;
        };
        if(violation == 0) {
            index = 0;
            while(index < $option.length) {
                if($option[index].selected == false) {
                    $option[index].disabled = true;
                }
                index++;
            };
            index = 0;
            while(index < $doc.getElementsByTagName('input').length) {
                $doc.getElementsByTagName('input')[index].readOnly = true;
                index++;
            };
            $doc.getElementById('js-contact').style.display = 'none';
            $doc.getElementById('js-contact-mod').style.display = 'block';
            $doc.getElementById('button').style.display = 'block';
            $doc.getElementById('button').disabled = false;
            $doc.getElementById('confirm').style.display = 'block';
        }
    };

    $doc.getElementById('js-contact').addEventListener('click',(e) => {contactClick(e)});

    //お問い合わせ編集
    const contactModClick = (e) => {
        // e.preventDefault();
        let index = 0;
        while(index < $violation.length){
            $violation[index].style.display = 'none';
            index++;
        };
        index = 0
        while(index < $option.length) {
            $option[index].disabled = false;
            index++;
        };
        index = 0;
        while(index < $doc.getElementsByTagName('input').length) {
            $doc.getElementsByTagName('input')[index].readOnly = false;
            index++;
        };
        $doc.getElementById('js-contact').style.display = 'block';
        $doc.getElementById('js-contact-mod').style.display = 'none';
        $doc.getElementById('button').style.display = 'none';
        $doc.getElementById('button').disabled = true;
        $doc.getElementById('confirm').style.display = 'none';
    };

    $doc.getElementById('js-contact-mod').addEventListener('click',(e) => {contactModClick(e)});

    //送信ボタン連打禁止
    let clickCount = 0;
    $doc.getElementById('button').onclick = () => {
        if (clickCount >= 1) {
            $doc.getElementById('button').disabled = true;
        }
        clickCount++;
    };

})();


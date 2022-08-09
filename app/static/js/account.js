(() =>{

    const $doc = document;
    const $violation = $doc.getElementsByClassName('violation')
    const $requiredViolation = $doc.getElementsByClassName('required-violation')

    //アカウント情報確認
    const signupClick = (e) => {
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
        let regex = /^[ァ-ヶー　 ]+$/;
        if(!($doc.getElementById('furigana').value == "") && regex.test($doc.getElementById('furigana').value) == false) {
            $doc.getElementById('furigana-format').style.display = 'block';
            violation++;
        }
        regex = /^\d{3}-?\d{4}$/;
        if(!($doc.getElementById('postal').value == "") && regex.test($doc.getElementById('postal').value) == false) {
            $doc.getElementById('postal-format').style.display = 'block';
            violation++;
        }
        regex = /^0\d{1,3}-?\d{2,4}-?\d{3,4}$/;
        if(!($doc.getElementById('tel').value == "") && regex.test($doc.getElementById('tel').value) == false) {
            $doc.getElementById('tel-format').style.display = 'block';
            violation++;
        }
        if(violation == 0) {
            index = 0;
            while(index < $doc.getElementsByTagName('input').length) {
                $doc.getElementsByTagName('input')[index].readOnly = true;
                index++;
            }
            $doc.getElementById('js-signup').style.display = 'none';
            $doc.getElementById('js-signup-mod').style.display = 'block';
            $doc.getElementById('button').style.display = 'block';
            $doc.getElementById('button').disabled = false;
            $doc.getElementById('confirm').style.display = 'block';
            $doc.getElementById('edit').style.display = 'none';
            $doc.getElementById('change-password').style.display = 'none';
            $doc.getElementById('cant-change').style.display = 'block';
        }
    };

    $doc.getElementById('js-signup').addEventListener('click',(e) => {signupClick(e)});

    //アカウント情報編集
    const signupModClick = (e) => {
        // e.preventDefault();
        let index = 0;
        while(index < $violation.length){
            $violation[index].style.display = 'none';
            index++;
        };
        // index = 0
        // while(index < $option.length) {
        //     $option[index].disabled = false;
        //     index++;
        // };
        index = 0;
        while(index < $doc.getElementsByTagName('input').length) {
            $doc.getElementsByTagName('input')[index].readOnly = false;
            index++;
        }
        $doc.getElementById('email').readOnly = true;
        $doc.getElementById('js-signup').style.display = 'block';
        $doc.getElementById('js-signup-mod').style.display = 'none';
        $doc.getElementById('button').style.display = 'none';
        $doc.getElementById('button').disabled = true;
        $doc.getElementById('confirm').style.display = 'none';
        $doc.getElementById('edit').style.display = 'block';
        $doc.getElementById('change-password').style.display = 'block';
        $doc.getElementById('cant-change').style.display = 'none';
    };

    $doc.getElementById('js-signup-mod').addEventListener('click',(e) => {signupModClick(e)});

    //送信ボタン連打禁止
    let clickCount = 0;
    $doc.getElementById('button').onclick = () => {
        if (clickCount >= 1) {
            $doc.getElementById('button').disabled = true;
        }
        clickCount++;
    };

})();


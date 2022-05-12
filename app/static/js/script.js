// System configeuration
function testWebP(callback) {
    var webP = new Image();
    webP.onload = webP.onerror = function () {
        callback(webP.height == 2);
    };
    webP.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA";
}
    
testWebP(function (support) {
    if (support == true) {
        document.querySelector('body').classList.add('webp');
    }else{
        document.querySelector('body').classList.add('no-webp');
    }
});;
// Watch system.js to customize

window.onload = () => {
    const button = document.querySelector('#delete_channel');
    const field = document.querySelector('#delete_agreement');
    const deleteForm = document.querySelector("#delete_form");
    const keyPhrase = "Я подтверждаю удаление аккаунта";
    if (field && button) {
        field.addEventListener('input', (e) => {
            if (field.value == keyPhrase) {
                button.classList.remove('disabled-button');
                button.disabled = false;
            } else {
                button.classList.add('disabled-button');
                button.disabled = true;
            }
        });
    }

    if (deleteForm && field) {
        deleteForm.addEventListener('submit', (e) => {
            if (field.value != keyPhrase) e.preventDefault();
        });
    }

    const popupInfo = document.querySelectorAll('.add-block-content__info');

    for (let i = 0; i < popupInfo.length; i++) {
        let img = popupInfo[i].querySelector('img');
        let div = popupInfo[i].querySelector('div');
    
        div.style.display = 'none';
    
        img.addEventListener('mouseover', (e) => {
            div.style.display = 'block';
        });

        img.addEventListener('mouseleave', (e) => {
            div.style.display = 'none';
        });
    }

    const videoBlocks = document.querySelectorAll('.channel-video-block');

    for (let vid of videoBlocks) {
        vid.querySelector('.channel-video-block__short').addEventListener('click', (e) => {
            let arrow = vid.querySelector('.channel-video-block__arrow').querySelector('img');
            let bl = vid.querySelector('.channel-video-block-detailed');

            arrow.style.transform = bl.style.display == 'none' ? 'rotateX(180deg)' : 'none';

            bl.style.display = bl.style.display == 'none' ? 'grid' : 'none';
        });
    }

    const nots_container = document.querySelector('.notifications');

    if (nots_container) {
        const nots = nots_container.children;

        for (let i = nots.length - 1; i >= 0; --i) {
            nots[i].style.animationDelay = (nots.length - i)*0.2 + 's';
            nots[i].style.animationName = 'slide-in-out';

            nots[i].addEventListener('click', (e) => {
                nots[i].style.opacity = 0;
            });
        }
    }
}


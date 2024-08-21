document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('textos');
    const articles = carousel.querySelectorAll('article');
    const btnPrev = document.getElementById('btn1');
    const btnNext = document.getElementById('btn2');

    let currentPosition = 0;

    function showArticle(index) {
        articles.forEach((article, i) => {
            article.style.display = i === index ? 'block' : 'none';
        });
    }

    function nextArticle() {
        currentPosition = (currentPosition + 1) % articles.length;
        showArticle(currentPosition);
        console.log('Next clicked, current position:', currentPosition);
    }

    function prevArticle() {
        currentPosition = (currentPosition - 1 + articles.length) % articles.length;
        showArticle(currentPosition);
        console.log('Prev clicked, current position:', currentPosition);
    }

    function addButtonListeners() {
        btnPrev.addEventListener('click', function(e) {
            e.preventDefault();
            prevArticle();
        });

        btnNext.addEventListener('click', function(e) {
            e.preventDefault();
            nextArticle();
        });
    }

    // Inicializa o carrossel
    showArticle(currentPosition);
    addButtonListeners();

    // Função para reajustar os botões em telas menores
    function adjustForSmallScreens() {
        if (window.innerWidth <= 449) {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'button-container-mobile';
            buttonContainer.style.display = 'flex';
            buttonContainer.style.justifyContent = 'center';
            buttonContainer.style.marginTop = '1em';

            const originalContainers = carousel.querySelectorAll('.button-container');
            originalContainers.forEach(container => container.style.display = 'none');

            buttonContainer.appendChild(btnPrev);
            buttonContainer.appendChild(btnNext);
            carousel.appendChild(buttonContainer);
        } else {
            const mobileContainer = carousel.querySelector('.button-container-mobile');
            if (mobileContainer) {
                const originalContainers = carousel.querySelectorAll('.button-container');
                originalContainers[0].appendChild(btnPrev);
                originalContainers[1].appendChild(btnNext);
                mobileContainer.remove();
                originalContainers.forEach(container => container.style.display = '');
            }
        }
    }

    // Chama a função de ajuste inicialmente e adiciona um listener para redimensionamento
    adjustForSmallScreens();
    window.addEventListener('resize', adjustForSmallScreens);
});

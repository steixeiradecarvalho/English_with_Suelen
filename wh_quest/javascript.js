document.addEventListener('DOMContentLoaded', () => {
    let draggedOption = null;
    const gaps = document.querySelectorAll('.gap');
    const dragOptions = document.querySelectorAll('.drag-option');
    const confettiContainer = document.getElementById('confetti-container');

    dragOptions.forEach(option => {
        option.addEventListener('dragstart', dragStart);
        option.addEventListener('dragend', dragEnd);
    });

    gaps.forEach(gap => {
        gap.addEventListener('dragover', dragOver);
        gap.addEventListener('drop', drop);
    });

    function dragStart(e) {
        draggedOption = this;
        setTimeout(() => this.style.visibility = 'hidden', 0); // Oculta o elemento sendo arrastado
    }

    function dragEnd() {
        setTimeout(() => this.style.visibility = 'visible', 0); // Retorna a visibilidade ao final do arrasto
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function drop(e) {
        e.preventDefault();
        const questionElement = this.closest('.question');
        const correctAnswer = questionElement.dataset.correctAnswer;
        const droppedAnswer = draggedOption.dataset.wh;


        if (droppedAnswer === correctAnswer) {
            // Remove o texto da lacuna (se houver)
            this.textContent = '';
            // Anexa o bloco arrastado diretamente à lacuna
            this.appendChild(draggedOption);
            this.classList.add('filled');
            this.classList.remove('gap'); // Remove a classe 'gap' para mudar o estilo se necessário
            draggedOption.style.cursor = 'default'; // Muda o cursor para 'default'
            draggedOption.draggable = false; // Impede que seja arrastado novamente
            draggedOption.classList.add('dropped'); // Adiciona uma classe para estilizar o bloco fixo
            checkGameCompletion();
            launchConfetti();
        } else {
            // Feedback visual de resposta incorreta (opcional)
            this.classList.add('incorrect'); // Adicione uma classe 'incorrect' para feedback visual
            setTimeout(() => {
                this.classList.remove('incorrect'); // Remove a classe 'incorrect' após um tempo
            }, 1000); // Remove a classe após 1 segundo
        }
        draggedOption = null; // Reseta draggedOption para evitar múltiplos drops acidentais
    }


    function launchConfetti() {
        const duration = 3000; // Duração total dos confetes em milissegundos
        const animationEnd = Date.now() + duration;
        const interval = 100; // Intervalo para criar novos confetes

        const confettiInterval = setInterval(function() {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(confettiInterval);
            }

            const particleCount = 50 * (timeLeft / duration); // Ajuste a quantidade de confetes ao longo do tempo

            for (let i = 0; i < particleCount; i++) {
                // Cria mais confetes no início e menos no final
                createConfetti();
            }
        }, interval);
    }


    function createConfetti() {
        const confetti = document.createElement('div');
        confetti.classList.add('confetti');
        confetti.style.left = Math.random() * 100 + 'vw'; // Posição horizontal aleatória
        confetti.style.animationDelay = Math.random() * 0.5 + 's'; // Delay aleatório para espalhar a animação
        confettiContainer.appendChild(confetti);

        // Remove o confete após a animação terminar para evitar acúmulo no DOM
        setTimeout(() => {
            confetti.remove();
        }, 3000); // Tempo correspondente à duração da animação confetti-fall
    }


    function checkGameCompletion() {
        if (document.querySelectorAll('.drag-option').length === 0) {
            alert('Parabéns! Você completou todas as questões!'); // Mensagem de parabéns ao completar tudo
        }
    }
});
function scrollSmoothTo() {
    const section = document.getElementById('about');
    const button = document.getElementById('scroll');

    button.addEventListener('click', ()=>{
        section.scrollIntoView({
          block: 'start',
          behavior: 'smooth'
        });
    });
  }
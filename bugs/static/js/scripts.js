function myFunction() {
    const links = document.getElementById('side-links');
    const hamburger = document.getElementById('icon');

    hamburger.addEventListener('click', () => {
        if(links.style.display == 'none'){links.style.display = 'block'}
        else{links.style.display = 'none'}
    })
  }
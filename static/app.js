$('form input[type="file"]').change(event => {
  let archives = event.target.files;
  if (archives.length === 0) {
    console.log('sem imagem pra mostrar')
  } else {
      if(archives[0].type === 'image/jpeg') {
        $('img').remove();
        let imagem = $('<img class="img-fluid">');
        imagem.attr('src', window.URL.createObjectURL(archives[0]));
        $('figure').prepend(imagem);
      } else {
        alert('Formato não suportado')
      }
  }
});
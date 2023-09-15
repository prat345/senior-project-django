var click = 1;
function showvid(url, index, button){
    var main_block = document.getElementById(`block-${index}`);
    if(click%2 !=0){
        url = url.split('/view?usp=drivesdk')[0];
        var vid_block = document.createElement(`div`);   
        vid_block.setAttribute('id',`vid-block-${index}`);
        vid_block.innerHTML=
        `<iframe src="${url}/preview"
            width="640" height="480" allow="autoplay fullscreen; picture-in-picture; xr-spatial-tracking;"></iframe>`;
        main_block.appendChild(vid_block);
        button.style.backgroundColor = 'rgb(5, 217, 5)';
        button.innerText = 'collaspe';
    }else{
        var vid_block = document.getElementById(`vid-block-${index}`);
        main_block.removeChild(vid_block);
        button.style.backgroundColor = null;
        button.innerText = 'view';
    }
    click++
    }
   
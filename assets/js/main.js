let click = 1;
function showvid(url, index, button){
    let main_block = document.getElementById(`block-${index}`);
    let vid_block = document.getElementById(`vid-block-${index}`);
    if(!vid_block){
        url = url.split('/view?usp=drivesdk')[0];
        vid_block = document.createElement(`div`);   
        vid_block.setAttribute('id',`vid-block-${index}`);
        let device_width = window.innerWidth;
        // device_width = 400;
        let width;
        if(device_width <= 450){
            width = device_width/1.05;
        }else{
            width = device_width/1.25;
        }
        let height = width/1.7; 
        vid_block.innerHTML=
        `<iframe src="${url}/preview"
            width=${width}px height=${height}px
            allow="autoplay fullscreen; picture-in-picture; xr-spatial-tracking;"></iframe>`;
        main_block.appendChild(vid_block);
        vid_block.style.textAlign ='center'
        button.style.backgroundColor = 'rgb(5, 217, 5)';
        button.style.color='White'
        button.innerText = 'close';
    }else{
        // var vid_block = document.getElementById(`vid-block-${index}`);
        main_block.removeChild(vid_block);
        button.style.backgroundColor = null;
        button.style.color=null
        button.innerText = 'view';
    }
    click++
    }
   
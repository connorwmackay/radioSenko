let is_playing = false;
let random_index = 0;
let audio;
let isOp = true;

const playIcon = $("<i class='fas fa-play-circle fa-3x'></i>");
const stopIcon = $("<i class='fas fa-stop-circle fa-3x'></i>");

$(() => {  
    const trackName = $("#radioTrackName");
    const urlParams = new URLSearchParams(window.location.search);
    is_radio_starting = true;

    if (urlParams.get('list')) {
        if (urlParams.get('list') != "none") {
            random_index = Math.floor(Math.random() * list_items.length);
            isOp = Math.floor(Math.random() * 3);
            requestTrack(list_items, isOp, random_index);

            $("#radioPlayBtn").click(() => {
                if (!is_playing) {
                    playTrack(list_items, isOp, random_index);
                    requestNextTrack();
                } else {
                    $("#radioPlayBtn").html(playIcon);
                    audio.pause()
                    is_playing = false;
                    trackName.text("Not started...");
                }
            });

            $("#radioSkipBtn").click(() => {
                if (is_playing) {
                    audio.pause();
                    playTrack(list_items, isOp, random_index);
                    requestNextTrack();
                }
            });
        }
    }
});

const waitFor = async(func) => {
    return new Promise((resolve) => {
        if (func()) {

        } else {
            setTimeout(async () => {
                await waitFor(func)
                resolve();
            }, 400);
        }
    })
}

function requestNextTrack() {
    old_index = random_index
    old_op = isOp
    while(random_index == old_index && old_op == isOp) {
        random_index = Math.floor(Math.random() * list_items.length);
        console.log(random_index)
        isOp = Math.floor(Math.random() * 3);
    }

    requestTrack(list_items, isOp, random_index);
}

function requestTrack(list, isOp, index) {
    console.log("Requesting track...");
    let op = " op";

    if (isOp != 0) {
        op = " ed";
    }

    $.getJSON(`/radio/request/${list[index]}/${op}`).then(() => {});
}

function playTrack(list, is_op, index) {
    let op = " op";
    if (is_op != 0) {
        op = " ed";
    }

    const trackName = $("#radioTrackName");

    $.getJSON(`/radio/check/${list_items[random_index]}/${op}`).then((data) => {
        if (data.is_downloaded) {
            $("#radioPlayBtn").html(stopIcon);
            is_playing = true;

            is_next_track_downloaded = false;
            audio = new Audio(`/static/downloads/${list[index]}${op}.mp4`);

            audio.addEventListener('ended', () => {
                console.log("ended...")
                playTrack(list_items, isOp, random_index)
                requestNextTrack();
            }, false);
            
            trackName.text(list[index] + op);
            audio.play();
        } else {
            trackName.text("Downloading...");

            setTimeout(() => {
                playTrack(list, is_op, index);
            }, 1000);
        }
    });
}
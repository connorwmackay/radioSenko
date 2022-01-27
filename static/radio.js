let is_playing = false;
let random_index = 0;
let audio;
let isOp = true;

const playIcon = $("<i class='fas fa-play-circle fa-3x'></i>");
const stopIcon = $("<i class='fas fa-stop-circle fa-3x'></i>");

$(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('list')) {
        if (urlParams.get('list') != "none") {
            random_index = Math.floor(Math.random() * list_items.length);
            isOp = Math.floor(Math.random() * 3);
            requestTrack(list_items, isOp, random_index);
            $("#radioPlayBtn").click(() => {
                if (!is_playing) {
                    $("#radioPlayBtn").html(stopIcon);

                    playTrack(list_items, isOp, random_index);
                    requestNextTrack();
                } else {
                    $("#radioPlayBtn").html(playIcon);
                    audio.pause()
                    is_playing = false;
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
    console.log("Playing...")
    is_playing = true;

    let op = " op";
    if (is_op != 0) {
        op = " ed";
    }

    is_next_track_downloaded = false;
    audio = new Audio(`/static/downloads/${list[index]}${op}.mp4`);

    audio.addEventListener('ended', () => {
        console.log("ended...")
        playTrack(list_items, isOp, random_index)
        requestNextTrack();
    }, false);

    const trackName = $("#radioTrackName");
    trackName.text(list[index] + op);
    audio.play();
}
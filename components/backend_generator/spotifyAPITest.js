var token = 'BQAOwOvbluqdB-5FtKhIhuAIKU4nhQQ-xhmkqcUkWbPx6wmfBbHg8acnmCpnctS4lF098UVhjFmmbdZhNuaWI2tdcr7Mhrvbksbalq-0avDlq5DYClw'; // if i accidentally publish this to ghithub ggs
var query = 'workout'; // IMPORTANT REMINDER: CHANGE THIS BEFORE TO THU 
var allSongs = [];

// kick!!!!!!!!!!!!! 
async function kickstart() {
  let playlists = await searchSpotify();
  await fetchTracksForPlaylists(playlists);
  let topTracks = calculateTopTracks(allSongs, 24); // top 24 cause issa album
  console.log(topTracks);
}

// playslikst seartchihg function
async function searchSpotify() {
  let response = await fetch(`https://api.spotify.com/v1/search?q=${query}&type=playlist`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  let data = await response.json();
  return data.playlists.items.map(playlist => ({ name: playlist.name, id: playlist.id }));
}

// playlists -> tracks and we push into all songs
async function fetchTracksForPlaylists(playlists) {
  await Promise.all(playlists.map(async (playlist) => {
    let tracks = await getPlaylistTracks(playlist.id); // uses func belo
    tracks.forEach(track => allSongs.push(track)); // PUSHG e into allSongs
  }));
}

// this is where we actually talk to spotify to get tracks
async function getPlaylistTracks(playlistId) {
  const response = await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks`, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const data = await response.json();
  return data.items.map(item => item.track ? item.track.id : null).filter(id => id !== null);
}

// let's se - the top 24 tracks
function calculateTopTracks(songs, limit) {
  let counts = songs.reduce((acc, id) => {
    acc[id] = (acc[id] || 0) + 1; // counting stuf - ???
    return acc;
  }, {});

  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1]) // sorting... somewhow 
    .slice(0, limit) //
    .map(track => ({ id: track[0], count: track[1] }));
}

kickstart(); // THE !!!! GOO ! GOO  GOO! ! ! 

// thank god done with this 


// BREAK DOWN FUNCTS INTO utils.js? -> sentiments from py -> main.js -> utils.js -> main.js -> py? 
import { useState } from 'react';
import './App.css'
import { TIMELINE } from './compiled_titles'

function App()
{

  const STORAGE = "timeline_index";

  function load_position(): number
  {
    const saved_index = localStorage.getItem(STORAGE);
    if (saved_index)
    {
      var val = parseInt(saved_index)
      val = Math.min(val, TIMELINE.entries.length);
      val = Math.max(0, val)
      return val
    }
    else
    {
      return 0
    }
  }

  const [curPosition, setCurPosition] = useState(load_position())

  function save_position(val: number)
  {
    val = Math.min(val, TIMELINE.entries.length);
    val = Math.max(0, val)
    localStorage.setItem(STORAGE, val.toString())
    setCurPosition(val)
  }

  function TimelineEntry({ index }: { index: number })
  {
    const entry = TIMELINE.entries[index];
    if (entry.series)
    {
      const series = TIMELINE.series[entry.series - 1]
      const seriesImage = `./posters/${series.poster}`
      return (
        <div className='entry'>
          <img src={seriesImage} ></img>
          <div className='entry-text'>
            <h3>{series.name}</h3>
            S{entry.season} E{entry.episode}: {entry.title}
          </div>
        </div>
      )
    }
    else
    {
      const movieImage = `./posters/${entry.poster}`
      return (
        <div className='entry'>
          <img src={movieImage} ></img>
          <h3>{entry.title}</h3>
        </div>
      )
    }
  }

  return (
    <>
      <div className='main-container'>
        <button onClick={() => { save_position(curPosition - 1) }}>Prev</button>

        <div>
          <div className='current-entry'>
            <TimelineEntry index={curPosition}></TimelineEntry>
          </div>

          <h2>Up Next</h2>


          <TimelineEntry index={curPosition + 1}></TimelineEntry>
          <TimelineEntry index={curPosition + 2}></TimelineEntry>
          <TimelineEntry index={curPosition + 3}></TimelineEntry>
          <TimelineEntry index={curPosition + 4}></TimelineEntry>
        </div>

        <button onClick={() => { save_position(curPosition + 1) }}>Next</button>
        <button onClick={() => { save_position(0) }}>Reset</button>
      </div>
    </>
  )
}

export default App

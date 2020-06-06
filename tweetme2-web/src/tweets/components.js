import React,  {useEffect, useState} from 'react'
import {loadTweets} from '../lookup'


export function TweetsList(props) {
  const [tweets, setTweets] = useState([])

  useEffect(()=>{
    const myCallback = (response, status) => {
      console.log(response, status)
      if (status === 200){
        setTweets(response)
      }
    }
    loadTweets(myCallback)
  }, [])
  return tweets.map((item, index)=>{
    return <Tweet tweet={item} key={`${index}-{item.id}`} className='my-5 py-5 border bg-white text-dark'/>
  })

}


export function ActionBtn(props){
  console.log(props)
  const {tweet, action} = props
  const className = props.className ? props.className : 'btn btn-primary'
  if (action === "like"){return <button className={className}>{tweet.likes} Likes</button>}
  else if (action === "unlike"){return <button className={className}>Unlike</button>}
  else if (action === "retweet"){return <button className={className}>Retweet</button>}
  else return <div>Fail</div>
}

export function Tweet(props){
  const {tweet} = props
  const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
  return <div className ={className}>
    <p>{tweet.id} - {tweet.content}</p>
    <div className='btn btn-group'><ActionBtn tweet={tweet} action={"like"}/></div>
    <div className='btn btn-group'><ActionBtn tweet={tweet} action={"unlike"} className={"btn btn-outline-primary"}/></div>
    <div className='btn btn-group'><ActionBtn tweet={tweet} action={"retweet"} className={"btn btn-outline-success"}/></div>
  </div>
}

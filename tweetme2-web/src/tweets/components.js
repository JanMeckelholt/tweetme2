import React,  {useEffect, useState} from 'react'
import {loadTweets} from '../lookup'

export function TweetsComponent(props){
  const handleSubmit = (event) => {
    event.preventDefault()
    console.log(event)
  }
  return <div className={props.className}>
    <div className='col-12 mb-3'>
      <from onSubmit={handleSubmit}>
        <textarea className='form-control' name='tweet'>
        </textarea>
        <button type='submit' className="btn btn-primary my-3">Tweet</button>
      </from>
    </div>
    <TweetsList/>
  </div>
}


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
  const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)
  const [userLike, setUserLike] = useState(tweet.userLike === true ? true : false)
  const className = props.className ? props.className : 'btn btn-primary'
  const handleClick = (event) => {
    event.preventDefault()
    if (action.type === 'like') {
      console.log(tweet.likes)
      if (!userLike){ //like
        setLikes(tweet.likes + 1)
        setUserLike(true)
      }
      else if (userLike){ //unlike
        setLikes(likes -1)
        setUserLike(false)
      }
    }
    if (action.type === 'unlike') {
      console.log(tweet.likes)
      setLikes(tweet.likes - 1)
    }
  }

  if (action.type === "like"){return <button className={className} onClick={handleClick}>{likes} Likes</button>}
  else if (action.type === "unlike"){return <button className={className} onClick={handleClick}>Unlike</button>}
  else if (action.type === "retweet"){return <button className={className}>Retweet</button>}
  else return <div>Fail</div>
}

export function Tweet(props){
  const {tweet} = props
  const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
  return <div className ={className}>
    <p>{tweet.id} - {tweet.content}</p>
    <div className='btn btn-group'><ActionBtn tweet={tweet} action={{type: "like", display: "Likes"}}/></div>
    <div className='btn btn-group'><ActionBtn tweet={tweet} action={{type: "unlike", display: "Unlike"}} className={"btn btn-outline-primary"}/></div>
    <div className='btn btn-group'><ActionBtn tweet={tweet} action={{type: "retweet", display: "Retweet"}} className={"btn btn-outline-success"}/></div>
  </div>
}

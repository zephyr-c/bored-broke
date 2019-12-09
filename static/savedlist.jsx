const DateHeader = (props) => {
    return <h2>{props.date}</h2>
}

class EventList extends React.Component {
    constructor(props){
        super(props);

        this.state = {events: []}

        this.getSaved = this.getSaved.bind(this)
        // setUser = this.setUser.bind(this)
    }

    getSaved(){
        $.get('/saved-events.json', {"userId": this.props.user}, (res) => {
            this.setState({events: res.saved})
        })
    }

    componentDidMount(){
        this.getSaved()
    }

    render(){
        const items = this.state.events.map(x => <li> {x} </li>);
        return <div>
                <ul>{items}</ul>
                </div>
    }
}

class EventTile extends React.Component {
    constructor(props){
        super(props)
    }

    render(){
        return(
            <div className="event-tile">
                <h2>{this.props.date}</h2>
                <a href={this.props.url}>{this.props.event_name}</a>
            </div>
            )
    }
}


function TileList(props) {
        const resultList = [];
        for (const currentResult of props.results) {
                resultList.push(
                    <EventTile key={currentResult.eventbrite_id}
                    url={currentResult.event_url}
                    event_name={currentResult.name}
                    event_data={currentResult}
                    user={props.user}
                    />
                );
        return <div>{resultList}</div>
    }
}

const user = $("#user").attr('value')

ReactDOM.render(<EventList user={user} />, document.getElementById('events'))
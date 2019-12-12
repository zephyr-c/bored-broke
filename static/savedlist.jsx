class Results extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        const dates = Object.entries(this.props.results);
        const resList = [];
        for (const obj of dates) {
            let header = obj[0];
            let items = obj[1];
            resList.push(<DateBox date={header} events={items} user={this.props.user} />);
        }
        return <div className="d-inline-block overflow-auto list-group list-group-flush">{resList}</div>
    }
}

class DateBox extends React.Component {
    constructor(props) {
        super(props);
    }

    render(){
        const eventList = [];
        const dateHeader = this.props.date;
        for (const currentResult of this.props.events) {
            eventList.push(<EventTile key={currentResult.eventbrite_id}
                    url={currentResult.event_url}
                    event_name={currentResult.name}
                    event_data={currentResult}
                    user={this.props.user}
                    />)
        }
        return <div className="py-2 list-group-item">
                <h3>{dateHeader}</h3>
                    {eventList}
                </div>
    }
}

class EventTile extends React.Component {
    constructor(props){
        super(props)
    }

    render(){
        // const saveButton = <SaveButton event={this.props.event_data} user={this.props.user} />
        return(
            <div className="event-tile">
                <h2>{this.props.date}</h2>
                <a href={this.props.url}>{this.props.event_name}</a>
                {this.props.user && <SaveButton event={this.props.event_data} user={this.props.user} />}
                 <div>
                    <p>{this.props.event_data.description}</p>
                </div>
            </div>
            )
    }
}

const user = $("#user").attr('value')

ReactDOM.render(<EventList user={user} />, document.getElementById('events'))
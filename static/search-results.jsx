// class ResultMap extends React.Component {
//     constructor(props){
//         super(props)
//     }

//     render(){
//         // initmap goes here?

//         return (
//             <div id="map"></div>
//             )
//     }
// }

class EventTile extends React.Component {
    constructor(props){
        super(props)
    }

    render(){

        return(
            <div className="event-tile">
                <a href={this.props.url}>{this.props.event_name}</a>
            </div>
            )
    }
}

// class SaveButton extends React.Component {
//     constructor(props){
//         super(props)
//     }

//     render(){

//         return()
//     }
// }

class EventList extends React.Component {
    constructor(props){
        super(props)
    }

    render(){
        const resultList = [];

        for (const currentResult of this.props.results) {
            resultList.push(
                <EventTile key={currentResult.eventbrite_id}
                url={currentResult.event_url}
                event_name={currentResult.name}
                />
            );
        }

        return(<div>{resultList}</div>)
    }
}

class PageContainer extends React.Component {
    constructor(props){
        super(props);

        this.state = { events: [] }
        this.updateEvents = this.updateEvents.bind(this);
    }

    getResults = () => {
        $.get('/test.json', this.updateEvents)
    }

    updateEvents(response) {
        const events = response.results;
        this.setState({ events: events });
    }

    componentDidMount() {
        this.getResults();
    }

    render(){

        return(
            <div>
            <EventList results={this.state.events} />
            </div>
            )
    }
}

ReactDOM.render(<PageContainer />, document.getElementById('container'))
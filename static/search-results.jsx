class ResultMap extends React.Component {
    constructor(props) {
        super(props);
        this.googleMapRef = React.createRef();
        }

    componentDidMount() {
        const googleMapScript = document.createElement('script')
        googleMapScript.src =
        `https://maps.googleapis.com/maps/api/js?key=AIzaSyBJ47ckkw31qEwG3As2oJzmGyT2SSoTCLU&callback=initMap`
        window.document.body.appendChild(googleMapScript);

        googleMapScript.addEventListener("load", () => {
            this.googleMap = this.initMap();
        });
    }

    initMap = () => {
        new window.google.maps.Map(this.googleMapRef.current, {
            zoom: 12,
            center: {
                lat: 37.7887459,
                lng: -122.4115852
            },
            disableDefaultUI: true,
        })
    }



    render(){

        return (
            <div
              id="map"
              ref={this.googleMapRef}
              style={{ width: '400px', height: '300px' }}
            />
            )
    }
}

class EventTile extends React.Component {
    constructor(props){
        super(props)
    }

    render(){

        return(
            <div className="event-tile">
                <a href={this.props.url}>{this.props.event_name}</a>
                <span>
                <SaveButton event={this.props.event_data} />
                </span>
            </div>
            )
    }
}

class SaveButton extends React.Component {
    constructor(props){
        super(props)
        this.state = { saved: false }
    }

    render(){

        return(
            <button className="save-btn" 
                id={ this.props.event.eventbrite_id }
                name={ this.props.event.eventbrite_id } 
                value={ this.props.event }>Save Event</button>
            );
    }
}

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
                event_data={currentResult}
                />
            );
        }

        return(<div>{resultList}</div>)
    }
}

class PageContainer extends React.Component {
    constructor(props){
        super(props);

        this.state = { events: [],
                       markers: [] }
        this.updateResults = this.updateResults.bind(this);
    }

    getResults = () => {
        $.get('/test.json', this.updateResults)
    }

    updateResults(response) {
        const events = response.results;
        const markers = response.markers;
        // console.log(markers)
        this.setState({ events: events,
                        markers: markers });
    }

    componentDidMount() {
        this.getResults();
    }

    render(){

        return(
            <div>
            <ResultMap places={this.state.markers} />
            <EventList results={this.state.events} />
            </div>
            )
    }
}

ReactDOM.render(<PageContainer />, document.getElementById('container'))
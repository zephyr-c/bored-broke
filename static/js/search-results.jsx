class ResultMap extends React.Component {
    constructor(props) {
        super(props);
        this.googleMapRef = React.createRef();
        }

        // {'name': event.name,
        // 'eventbrite_id': event.id,
        // 'event_url': event.url,
        // 'date': event.startdatetime,
        // 'category': event.cateogry,
        // 'description': event.description,
        // 'location': event.address,
        // 'coords': {
        //      'lat': e['venue']['latitude'],
        //      'lng': e['venue']['longitude']},
        // }

    componentDidMount() {
        const googleMapScript = document.createElement('script')
        googleMapScript.src =
        `https://maps.googleapis.com/maps/api/js?key=AIzaSyAjzcFuaU59MQFb9_uODWbobJDnQ3Zm_A0`
        window.document.body.appendChild(googleMapScript);

        googleMapScript.addEventListener("load", () => {
            this.googleMap = this.initMap();
        });
        console.log(this.props.results)
    }

    initMap = () =>
        new window.google.maps.Map(this.googleMapRef.current, {
            zoom: 12,
            center: {
                lat: 37.7887459,
                lng: -122.4115852
            },
        });

    createMarkers = () => {
            let locations = [];
            for (const place of this.props.results){
                let marker = place
                marker.coords.lat = parseFloat(marker.coords.lat);
                marker.coords.lng = parseFloat(marker.coords.lng);
                locations.push(marker);
            };
            this.googleMap.panTo(locations[0].coords)

            const markers = [];
            for (const location of locations) {
                // console.log(location.description);
                markers.push(new window.google.maps.Marker({
                    position: location.coords,
                    title: location.name,
                    map: this.googleMap,
                    info: location.description,
                    icon: {
                        url: '/static/img/marker.svg',
                        scaledSize: {
                            width: 30,
                            height: 30
                        }
                    }
                }));
            }

            for (const marker of markers) {
                const markerInfo = (`
                  <h3>${marker.title}</h3>
                  <p>
                    ${marker.info}
                  </p>
                `);

                const infoWindow = new google.maps.InfoWindow({
                    content: markerInfo,
                    maxWidth: 200
                });

                marker.addListener("click", () => {
                    infoWindow.open(this.googleMap, marker);
                });

                marker.addListener("dblclick", () => {
                    infoWindow.close(this.googleMap, marker);
                });

            }
    }

    componentDidUpdate(prevProps) {
        if (this.props.places != prevProps.places) {
            this.createMarkers();
        }
    }

    render(){
        return (
            <div
              id="map"
              ref={this.googleMapRef}
              style={{ width: '50vw', height: '100vh' }}
            />
            )
    }
}

class SaveButton extends React.Component {
    constructor(props){
        super(props)
        this.state = { saved: false }
        this.checkSaved = this.checkSaved.bind(this)
        this.saveEvent = this.saveEvent.bind(this)
    }

    checkSaved() {
    let data = {"evtId": this.props.event.eventbrite_id, "userId": this.props.user,
                "checkSave": true};
    $.get("/saved-events.json", data, (response) => {
        this.setState({ saved: response.saved });
        });
    }

    saveEvent(evt) {
        $.post("/save-event", {"evtID": evt.target.id}, (response) =>
            response.status === 'success' ? this.setState({ saved: true }) :
            alert("Something Went Wrong"));
    }


    componentDidMount() {
        this.checkSaved();
    }


    render(){
        const notSaved = <button onClick={ this.saveEvent }
                className="save-btn"
                id={ this.props.event.eventbrite_id }
                name={ this.props.event.eventbrite_id }>Save Event</button>;

        const isSaved = <button className="save-btn"
                id={ this.props.event.eventbrite_id }
                name={ this.props.event.eventbrite_id }
                disabled={true}>Event Saved!</button>;

        return(
            <span>
            { this.state.saved === true ? isSaved : notSaved }
            </span>
            )
        }
    }

const DateHeader = (props) => {
    return <h2>{props.date}</h2>
}

class EventList extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        const resultList = [];
        const dates = Object.keys(this.props.results);
        const events = this.props.results;
        const user = this.props.user;
        for (const date of dates){
        resultList.push(
            <div>
            <DateHeader date={date} />
            <TileList results={events[date]} user={user} />
            </div>)
        }
    return(<div>{resultList}</div>)
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


class SearchForm extends React.Component {
    constructor(props){
        super(props);
        var today = new Date()
        this.state = { where: '',
                       when: '',
                       what: ''}

        this.handleInput = this.handleInput.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    };

    handleInput(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        this.setState({
            [name]: value
            });
    }

    handleSubmit(event) {
        event.preventDefault();
        const query = {
            where: this.state.where,
            when: this.state.when,
            what: this.state.what,
        };
        this.props.searchEvents(query);
    }



    render(){
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    What:
                    <input
                    name="what"
                    type="text"
                    value={this.state.what}
                    onChange={this.handleInput} />
                </label>
                <label>
                    Where:
                    <input
                    name="where"
                    type="text"
                    value={this.state.where}
                    onChange={this.handleInput} />
                </label>
                <label>
                    When:
                    <select
                    name="when"
                    value={this.state.when}
                    onChange={this.handleInput}>
                        <option value="today">Today</option>
                        <option value="tomorrow">Tomorrow</option>
                        <option value="this_weekend">This Weekend</option>
                        <option value="next_week">Next Week</option>
                    </select>
                </label>
                <input type='submit' value="Search" />
            </form>

            );
    }
}

class PageContainer extends React.Component {
    constructor(props){
        super(props);

        this.state = { events: [],
                       results: false,
                       markers: [],
                       status: '',
                       dates: {},
                       user: null }
        this.updateResults = this.updateResults.bind(this);
        this.searchEvents = this.searchEvents.bind(this);
    }

    searchEvents(query) {
        $.get('/test.json', query, this.updateResults)
    }

    updateResults(response) {
        const events = response.results;
        const markers = response.markers;
        const user = response.user_id
        const status = response.status;
        this.setState({ events: events,
                        results: true,
                        markers: markers,
                        status: status,
                        dates: response.sorted,
                        user: user });
    }

    render(){
        const searchResults = <EventList status={this.state.status} results={this.state.dates}
                       user={this.state.user} />
        const resultMap = <ResultMap places={this.state.markers} results={this.state.events} />

        return(
            <div>
            <section>
            <SearchForm searchEvents={this.searchEvents}  />
            <ResultMap places={this.state.markers} results={this.state.events} />
            </section>
            {this.state.results && searchResults}
            </div>
            )
    }
}

ReactDOM.render(<PageContainer />, document.getElementById('results'))
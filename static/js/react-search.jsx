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
                let d = new Date(location.date);
                let date = d.toDateString()
                markers.push(new window.google.maps.Marker({
                    position: location.coords,
                    title: location.name,
                    map: this.googleMap,
                    info: location.description,
                    address: location.location,
                    date: date,
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
                <div class="overflow-auto">
                  <h5>${marker.title}</h5>
                  <p class="text-muted">${marker.date}</p>
                  <p class="text-muted">${marker.address}</p>
                  <hr />
                  <p>
                    ${marker.info}
                  </p>
                  </div>
                `);

                const infoWindow = new google.maps.InfoWindow({
                    content: markerInfo,
                    maxWidth: 400
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
              className="w-100 h-100 border border-primary border-3"
              ref={this.googleMapRef}
              // style=
            />
            )
    }
}

class SaveButton extends React.Component {
    constructor(props){
        super(props);
        this.evtID = this.props.event.eventbrite_id
        this.state = { saved: false }
        this.checkSaved = this.checkSaved.bind(this)
        this.saveEvent = this.saveEvent.bind(this)
    }

    checkSaved() {
    let data = {"evtId": this.props.event.eventbrite_id, "userId": this.props.user,
                "checkSave": true};
    $.get("/saved-events.json", data, (response) => {
        this.setState({ saved: response.status });
        });
    }

    saveEvent(e) {
        const tgt = $(e.target);
        tgt.addClass("fa-spin");
        $.post("/save-event", {"evtID": this.evtID}, (response) =>
            response.status === 'success' ? this.setState({ saved: true }) :
            alert("Something Went Wrong"));
    }


    componentDidMount() {
        this.checkSaved();
    }


    render(){
        const notSaved = <a className="btn" id={ this.evtID } href="#"
                        onClick={this.saveEvent}><i className="far fa-heart"></i></a>;

        const isSaved = <a className="btn" id={this.evtID} href="#"
                        disabled={true}><i className="fas fa-heart"></i></a>;

        return(
            <span>
            { this.state.saved === true ? isSaved : notSaved }
            </span>
            )
        }
    }

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
        return <div className="overflow-auto list-group list-group-flush">{resList}</div>
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
                <a href={this.props.url} target="_blank">{this.props.event_name}</a>
                {this.props.user && <SaveButton event={this.props.event_data} user={this.props.user} />}
                 <div>
                    <p>{this.props.event_data.description}</p>
                </div>
            </div>
            )
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
            <form className="pt-3 pb-2" onSubmit={this.handleSubmit}>
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
        $.get('/event-search.json', query, this.updateResults)
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
        const searchResults = <Results status={this.state.status} results={this.state.dates}
                       user={this.state.user} />
        const resultMap = <ResultMap places={this.state.markers} results={this.state.events} />

        return(
            <div className="row">
                <div className="col-12">
                    <SearchForm searchEvents={this.searchEvents}  />
            <div className="row">
                <div className="col-8 col-sm-6 vw-50 vh-100">
                    <ResultMap places={this.state.markers} results={this.state.events} />
                </div>
                <div className="col-4 col-sm-6 vw-50 vh-100 overflow-auto">
                {this.state.results && searchResults}
                </div>
            </div>
            </div>
            </div>
            )
    }
}

ReactDOM.render(<PageContainer />, document.getElementById('results'))
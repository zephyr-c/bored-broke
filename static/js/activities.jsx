const ActivityTile = (props) => {
    return (
        <div className="card-img-overlay d-flex d-flex-row">
            <h5 className="card-title display-1 img-text" id="head">{props.suggestion}</h5>
            <h1 className="card-text p-1 text-shadow-lg img-text align-self-center" id="body">{props.description}</h1>
            <ChoiceButton function={props.getActivity} name="New Choice" />
            </div>
            );
}

const ChoiceButton = (props) => {
    return(
            <button className="btn-sm btn-secondary mt-5 align-self-end"
            onClick={props.function}>{props.name}</button>
        )
}


class ActivityPageContainer extends React.Component{
    constructor(props){
    super(props);

    this.state = { activity: 'Go to the Library',
                   description: 'Check Out Some Books',
                   img: 'https://cdn.pixabay.com/photo/2015/07/27/20/16/book-863418_1280.jpg'}
    this.newActivity = this.newActivity.bind(this);
}

getActivity = () => {
    $.get('/activities.json', this.newActivity)
}

newActivity(response) {
    const activity = response.activity;
    const description = response.description;
    const img = response.img
    this.setState({ activity: activity, description: description, img: img});
}

render() {

    return(
        <div className="card bg-dark text-white text-center w-75 h-75 p-3">
        <img src={this.state.img} className="card-img img-fluid" alt="..." />
        <ActivityTile suggestion={this.state.activity}
        description={this.state.description} getActivity={this.getActivity} newActivity={this.newActivity} />
        </div>)
}

}

ReactDOM.render(<ActivityPageContainer />, document.getElementById('root'))
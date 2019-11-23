class ActivityTile extends React.Component {
    constructor(props){
        super(props);
    }

    render() {
        return (
            <div className="tile">
            <h1>{this.props.suggestion}</h1>
            <h2>{this.props.description}</h2>
            </div>
            );
    }
}


class ActivityPageContainer extends React.Component{
    constructor(props){
    super(props);

    this.state = { activity: 'Go to the Library',
                   description: 'Check Out Some Books'}
    this.newActivity = this.newActivity.bind(this);
}

getActivity = () => {
    $.get('/activities.json', this.newActivity)
}

newActivity(response) {
    const activity = response.activity;
    const description = response.description;
    this.setState({ activity: activity, description: description});
}

render() {

    return(
        <div>
        <ActivityTile suggestion={this.state.activity}
        description={this.state.description} newActivity={this.newActivity} />
        <button onClick={this.getActivity}>New Choice</button>
        </div>)
}

}

ReactDOM.render(<ActivityPageContainer />, document.getElementById('container'))
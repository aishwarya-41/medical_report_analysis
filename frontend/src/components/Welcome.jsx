import { Link } from "react-router"

const Welcome = () => {
  return (
    <div className="home-container">
       <section className="hero-section">
        <h1 className="hero-title">
          Your Personal AI <br /> Medical Assistant
        </h1>
        <p className="hero-subtitle">
          Understand your health better. Upload your medical reports and get instant,
          easy-to-understand analysis and answers to your health questions.
        </p>
        <Link to="/upload" className="cta-button">
          Analyze Report Now
        </Link>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <h2 className="section-title">How It Works</h2>
        <div className="steps-container">
          <div className="step-item">
            <div className="step-number">1</div>
            <p className="step-text">Upload your PDF report</p>
          </div>
          <div className="step-item">
            <div className="step-number">2</div>
            <p className="step-text">AI analyzes the data</p>
          </div>
          <div className="step-item">
            <div className="step-number">3</div>
            <p className="step-text">Get insights & ask questions</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Welcome

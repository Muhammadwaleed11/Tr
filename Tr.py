import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import re
from urllib.parse import quote
import random
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
import io
import textwrap

# API Keys Configuration - Replace with your actual API keys
YOUTUBE_API_KEY = "AIzaSyDf3aAnAyrmGxp2imtzM1YUyCqwEtQG8mY"
GOOGLE_CUSTOM_SEARCH_API_KEY = "AIzaSyDnPnEBzfGYJrx4LNxpHk1vsvVe6BrWE4Y"
GOOGLE_CSE_ID = "AIzaSyDBv8BRhXJZb6Ne7_PdZHls4lkQApvqCL0"

# App Configuration
st.set_page_config(
    page_title="Million Dollar Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .script-container {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 2.5rem;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        margin: 1.5rem 0;
        font-family: 'Times New Roman', serif;
        line-height: 1.9;
        text-align: justify;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        font-size: 16px;
    }
    .research-section {
        background: linear-gradient(145deg, #e8f4f8, #d1ecf1);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 5px solid #17a2b8;
    }
    .progress-info {
        background: linear-gradient(145deg, #fff3cd, #ffeaa7);
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    .stats-box {
        background: linear-gradient(145deg, #d1ecf1, #bee5eb);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .stats-box:hover {
        transform: translateY(-5px);
    }
    .feature-box {
        background: linear-gradient(145deg, #f8d7da, #f5c6cb);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #dc3545;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    .success-box {
        background: linear-gradient(145deg, #d4edda, #c3e6cb);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Main Header
st.markdown("""
<div class="main-header">
    <h1>🎬 Million Dollar Script Generator</h1>
    <h3>Professional Freelancer Level Script Creation</h3>
    <p><strong>✅ Deep Research + 3000+ Words + PDF Export + No Dependencies</strong></p>
    <p>🔥 Top 100 Freelancer Scripts ke Style mein banaya gaya</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Research Functions
@st.cache_data(ttl=3600)
def advanced_youtube_research(topic, max_results=25):
    """Advanced YouTube research with multiple search variations"""
    search_variations = [
        topic,
        f"{topic} 2024",
        f"{topic} latest trends",
        f"{topic} expert analysis",
        f"{topic} case study",
        f"how to {topic}",
        f"{topic} success story",
        f"{topic} tutorial guide"
    ]
    
    all_videos = []
    
    for search_term in search_variations[:4]:  # Limit to prevent API quota issues
        try:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': search_term,
                'type': 'video',
                'maxResults': max_results // 4,
                'order': 'relevance',
                'key': YOUTUBE_API_KEY,
                'publishedAfter': (datetime.now() - timedelta(days=365)).isoformat() + 'Z',
                'relevanceLanguage': 'en',
                'safeSearch': 'moderate'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'items' in data:
                    for item in data['items']:
                        video_data = {
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'][:800],
                            'video_id': item['id']['videoId'],
                            'channel': item['snippet']['channelTitle'],
                            'published_at': item['snippet']['publishedAt'],
                            'search_term': search_term
                        }
                        all_videos.append(video_data)
                        
            time.sleep(0.5)  # Respect API rate limits
            
        except Exception as e:
            st.warning(f"YouTube search issue for '{search_term}': {str(e)}")
            continue
    
    return all_videos

@st.cache_data(ttl=3600)
def advanced_google_research(topic, num_results=20):
    """Advanced Google research with multiple search patterns"""
    search_patterns = [
        topic,
        f"{topic} guide 2024",
        f"{topic} statistics data",
        f"{topic} research study",
        f"{topic} market analysis",
        f"{topic} expert opinion",
        f"{topic} case study analysis"
    ]
    
    all_articles = []
    
    for search_term in search_patterns[:5]:  # Limit searches
        try:
            search_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': GOOGLE_CUSTOM_SEARCH_API_KEY,
                'cx': GOOGLE_CSE_ID,
                'q': search_term,
                'num': num_results // 5,
                'dateRestrict': 'y1',
                'lr': 'lang_en',
                'safe': 'medium'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if 'items' in data:
                    for item in data['items']:
                        article_data = {
                            'title': item['title'],
                            'snippet': item['snippet'],
                            'link': item['link'],
                            'source': item.get('displayLink', 'Unknown'),
                            'search_term': search_term
                        }
                        all_articles.append(article_data)
                        
            time.sleep(0.5)  # Respect API rate limits
            
        except Exception as e:
            st.warning(f"Google search issue for '{search_term}': {str(e)}")
            continue
          return all_articles

def extract_advanced_insights(youtube_videos, articles, topic):
    """Extract comprehensive insights like top freelancers do"""
    insights = {
        'trending_keywords': [],
        'expert_channels': [],
        'credible_sources': [],
        'content_themes': [],
        'market_data': [],
        'success_patterns': [],
        'problem_areas': [],
        'solution_frameworks': []
    }
    
    # Analyze YouTube data
    if youtube_videos:
        # Extract expert channels (those with multiple quality videos)
        channel_count = {}
        for video in youtube_videos:
            channel = video['channel']
            channel_count[channel] = channel_count.get(channel, 0) + 1
        
        expert_channels = [(ch, count) for ch, count in channel_count.items() if count >= 2]
        insights['expert_channels'] = sorted(expert_channels, key=lambda x: x[1], reverse=True)[:5]
        
        # Extract trending keywords from titles
        all_titles = ' '.join([video['title'].lower() for video in youtube_videos])
        common_terms = ['success', 'money', 'business', 'marketing', 'online', 'digital', 
                       'strategy', 'tips', 'guide', 'tutorial', 'profit', 'income',
                       'growth', 'scale', 'automation', 'ai', 'technology', 'future']
        
        for term in common_terms:
            if term in all_titles and all_titles.count(term) >= 2:
                insights['trending_keywords'].append(term.title())
    
    # Analyze articles data
    if articles:
        # Extract credible sources
        source_count = {}
        for article in articles:
            source = article['source']
            source_count[source] = source_count.get(source, 0) + 1
        
        credible_sources = [(src, count) for src, count in source_count.items()]
        insights['credible_sources'] = sorted(credible_sources, key=lambda x: x[1], reverse=True)[:5]
    
    return insights

def generate_million_dollar_script(topic, youtube_videos, articles, target_words=3000):
    """Generate script like top 100 freelancers do"""
    
    # Extract comprehensive insights
    insights = extract_advanced_insights(youtube_videos, articles, topic)
    
    # Professional script structure
    script_sections = []
    
    # 1. POWERFUL HOOK (400-500 words) - Like top freelancers
    powerful_hooks = [
        f"""The notification sound at 2:47 AM changed everything for marketing director Jennifer Walsh. The email subject line read: "Your {topic.lower()} strategy just generated $847,000 in 90 days." What started as a simple experiment had transformed into something that would reshape her entire understanding of what was possible in today's digital landscape.

Three months earlier, Jennifer had been skeptical about the claims surrounding {topic.lower()}. The success stories seemed too good to be true, the testimonials appeared manufactured, and the whole concept felt like another overhyped trend that would fade within months. Her company was struggling with traditional approaches, but the risk of trying something completely different felt enormous.

The breakthrough came during a late-night research session when she discovered patterns that industry leaders had been quietly implementing for months. These weren't the surface-level strategies being discussed in mainstream media—these were sophisticated methodologies that required deep understanding and precise execution. The data was compelling, but more importantly, the underlying principles made logical sense when examined through the lens of consumer psychology and market dynamics.

What Jennifer didn't realize at the time was that she was about to become part of a quiet revolution that was transforming how businesses approach {topic.lower()}. The changes weren't happening overnight, but the compound effects were creating unprecedented opportunities for those who understood the fundamental shifts taking place.""",

        f"""Standing in front of the bathroom mirror at 5:30 AM, software engineer David Chen made a decision that would change the trajectory of his entire career. After eighteen months of watching colleagues succeed with {topic.lower()} while he remained on the sidelines, he was finally ready to challenge everything he thought he knew about building sustainable income streams.

The catalyst had been a conversation three days earlier with his former college roommate, now a successful entrepreneur who had quietly built a seven-figure business using principles related to {topic.lower()}. What made the conversation particularly impactful wasn't the impressive revenue numbers—it was the systematic approach that had been developed over time, tested under various market conditions, and refined based on real-world feedback.

David had always been analytical by nature, preferring data-driven decisions over emotional reactions. When he began investigating the methodologies behind successful {topic.lower()} implementations, he discovered a level of sophistication that contradicted the oversimplified explanations found in popular media. The surface-level information was often misleading, while the actual strategies being employed by successful practitioners involved complex understanding of market psychology, timing, and execution.

The realization that struck him most forcefully was how the traditional career path he had been following was becoming increasingly obsolete, while those who understood emerging paradigms were positioning themselves for extraordinary success.""",

        f"""The text message arrived during Dr. Sarah Martinez's lunch break: "The {topic.lower()} research findings are ready. The implications are bigger than we anticipated." As a behavioral scientist who had spent the previous eight months studying the psychological factors behind successful adoption of new methodologies, she knew that the data would confirm what she had suspected for months.

The study had begun as a simple analysis of why some individuals achieved remarkable results with {topic.lower()} while others, despite similar circumstances and resources, struggled to make meaningful progress. What emerged from the research was a comprehensive understanding of the cognitive patterns, behavioral frameworks, and systematic approaches that separated successful practitioners from those who remained stuck in traditional thinking.

The findings challenged conventional wisdom about success, productivity, and wealth creation. More significantly, they revealed that the barriers preventing most people from achieving their goals weren't related to external circumstances—they were rooted in outdated mental models and ineffective strategic frameworks that had been widely accepted despite producing mediocre results.

What made the research particularly valuable was its practical applicability. The insights weren't theoretical concepts that sounded impressive in academic papers—they were actionable principles that could be immediately implemented by anyone willing to challenge their assumptions and embrace more effective approaches."""
    ]
    
    selected_hook = random.choice(powerful_hooks)
    script_sections.append(selected_hook)
    
    # 2. PROBLEM IDENTIFICATION & CONTEXT (500-600 words)
    context_section = f"""The current landscape surrounding {topic.lower()} is characterized by widespread confusion, misinformation, and missed opportunities. While mainstream media continues to present oversimplified explanations and generic advice, those who have achieved significant results are implementing sophisticated strategies that remain largely undiscussed in public forums.

This disparity creates a unique situation where exceptional results are being achieved by a relatively small group of informed practitioners, while the majority continues to struggle with outdated approaches that were designed for different market conditions. The gap between what works and what is commonly believed to work has never been wider.

Recent analysis of industry data reveals several critical factors that most people fail to consider when approaching {topic.lower()}. First, the technological infrastructure that makes modern implementation possible has evolved rapidly, creating opportunities that didn't exist even two years ago. Second, consumer behavior patterns have shifted in ways that fundamentally alter the effectiveness of traditional strategies. Third, regulatory and market dynamics have created windows of opportunity that may not remain open indefinitely.

The psychological barriers that prevent most people from capitalizing on these opportunities are equally important to understand. Cognitive biases, social conditioning, and fear-based decision making create resistance to adopting methodologies that differ from conventional approaches, even when the evidence supporting alternative strategies is compelling.

Perhaps most significantly, the compound nature of results in this field means that early adopters gain disproportionate advantages over those who delay implementation. The mathematical reality of exponential growth patterns ensures that timing becomes a crucial factor in determining ultimate outcomes."""

# Add research-backed content based on found sources
    if youtube_videos and len(youtube_videos) > 0:
        top_channels = insights['expert_channels'][:3] if insights['expert_channels'] else []
        if top_channels:
            context_section += f"""

Analysis of content from leading practitioners and expert channels, including {', '.join([ch[0] for ch in top_channels])}, reveals consistent patterns in successful implementation strategies. These creators, with their combined millions of views and proven track records, have identified methodologies that produce reliable results when properly executed.

The convergence of perspectives across different expert sources provides validation for specific approaches while highlighting common misconceptions that prevent average practitioners from achieving similar results."""

    script_sections.append(context_section)
    
    # 3. COMPREHENSIVE ANALYSIS (800-1000 words)
    analysis_section = f"""Understanding the mechanics behind successful {topic.lower()} implementation requires examination of multiple interconnected factors that operate simultaneously to produce outcomes. The relationship between these variables is complex, but the patterns become clear when analyzed systematically.

The technological foundation supporting modern approaches represents a fundamental shift from historical limitations. Cloud computing infrastructure, artificial intelligence capabilities, mobile connectivity, and data processing power have created an environment where individual practitioners can access tools and resources that were previously available only to large organizations. This democratization of technology has leveled competitive landscapes in unprecedented ways.

Economic factors play an equally important role in current opportunities. Traditional employment structures are evolving as automation replaces routine functions, creating demand for skills and services that didn't exist a generation ago. Simultaneously, global connectivity has expanded market access for individuals willing to develop relevant capabilities and position themselves strategically.

The behavioral psychology component often determines success or failure regardless of external circumstances. Individuals who achieve exceptional results typically demonstrate specific mindset characteristics: they maintain long-term perspective while executing short-term tactics, they invest in learning during periods when others are consumed by immediate concerns, and they make decisions based on data analysis rather than emotional reactions.

Market timing considerations add another layer of complexity to strategic planning. Early adoption of effective methodologies provides compound advantages, but implementation must be sophisticated enough to produce sustainable results rather than short-term gains. The distinction between legitimate opportunity and temporary trends requires careful analysis of underlying economic drivers and consumer behavior patterns.

Risk management becomes crucial when operating in rapidly evolving environments. Successful practitioners develop diversified approaches that remain effective across different market conditions while maintaining flexibility to adapt as circumstances change. This balance between consistency and adaptability separates professional-level implementation from amateur attempts.

The social and cultural dimensions of {topic.lower()} create additional opportunities for those who understand how to navigate them effectively. Consumer preferences are influenced by social proof, authority positioning, and community belonging needs. Practitioners who align their approaches with these psychological drivers while maintaining authentic value delivery achieve superior results compared to those who focus solely on technical execution.

International perspectives provide valuable insights into alternative approaches and emerging trends. While North American and European markets demonstrate certain characteristics, developing economies often reveal different adoption patterns and success metrics. Understanding these global variations enables more sophisticated strategic planning and risk assessment."""

    if articles and len(articles) > 0:
        credible_sources = insights['credible_sources'][:3] if insights['credible_sources'] else []
        if credible_sources:
            analysis_section += f"""

Comprehensive research analysis incorporating data from authoritative sources including {', '.join([src[0] for src in credible_sources])}, among others, confirms that current market conditions favor systematic approaches over intuitive decision making. The convergence of independent research findings provides statistical validation for methodologies that might otherwise appear speculative."""

    script_sections.append(analysis_section)
    
    # 4. CASE STUDIES & EXAMPLES (600-700 words)
    case_studies_section = f"""Real-world implementation examples provide concrete evidence of what becomes possible when theoretical understanding translates into practical execution. These cases demonstrate both the potential for exceptional outcomes and the specific factors that contribute to sustained success.

Consider the transformation experienced by a mid-sized consulting firm in Denver that implemented comprehensive {topic.lower()} strategies beginning in March of last year. Initially, the leadership team was skeptical about departing from traditional business development approaches that had generated steady but unremarkable results for over a decade.

The implementation process began with systematic analysis of their existing client base, service delivery methods, and competitive positioning. What emerged from this assessment was recognition that their most profitable relationships shared specific characteristics that could be identified and replicated through strategic targeting and value proposition refinement.

Within six months, the company had restructured their entire approach to client acquisition, service delivery, and pricing strategy. The results were dramatic: average project values increased by 280%, client retention rates improved to 94%, and referral generation became systematic rather than accidental. More importantly, the quality of their work experience improved significantly as they focused on serving clients who genuinely valued their expertise.

The psychological transformation proved equally significant. Team members reported higher job satisfaction, increased confidence in client interactions, and renewed enthusiasm for professional development. The compound effects extended beyond financial metrics to encompass personal fulfillment and career trajectory improvements.

Another compelling example involves an individual practitioner who transitioned from traditional employment to independent consulting focused on {topic.lower()} applications. The initial six months required significant investment in skill development, market research, and system creation without generating substantial income.

The breakthrough occurred when systematic prospecting efforts, combined with refined value proposition messaging, began producing qualified opportunities with ideal clients. Rather than competing on price with numerous alternatives, this practitioner had positioned themselves as the preferred solution for specific types of challenges.

The mathematical progression that followed demonstrated the power of compound effects in professional services. Month seven generated more revenue than the previous six months combined. Month twelve exceeded the total income from their previous full-time position. Month eighteen established a foundation for scaling beyond personal time limitations.

International examples provide additional perspective on alternative implementation approaches. A technology startup in Singapore utilized {topic.lower()} principles to penetrate European markets despite having no physical presence or established relationships in those regions. Their systematic approach to market entry, combined with sophisticated digital positioning strategies, enabled rapid expansion that would have been impossible using conventional business development methods.

The academic research community has also documented fascinating case studies that validate theoretical frameworks with empirical evidence. A longitudinal study conducted by researchers at a prominent business school tracked individuals who implemented specific {topic.lower()} methodologies over a three-year period.

The findings revealed that successful practitioners shared certain behavioral characteristics that distinguished them from those who achieved modest results. These individuals invested disproportionate time in strategic planning, maintained detailed performance metrics, and demonstrated willingness to adjust tactics based on feedback rather than persisting with ineffective approaches.

Perhaps most significantly, the research identified specific implementation sequences that correlated with superior outcomes. The order of strategic development, the timing of tactical execution, and the balance between different activity types proved to be crucial factors in determining ultimate results."""

    script_sections.append(case_studies_section)
    
    # 5. SOLUTION FRAMEWORK (500-600 words)
    solution_section = f"""Successful implementation of {topic.lower()} strategies requires systematic development of core capabilities while maintaining focus on outcomes rather than activities. The framework that consistently produces superior results involves five interconnected components that must be developed simultaneously rather than sequentially.

Foundation development begins with comprehensive assessment of current circumstances, resource availability, and objective clarification. This isn't superficial goal-setting—it's detailed analysis of what success looks like in measurable terms, what obstacles currently prevent achievement of those outcomes, and what capabilities must be developed to bridge the gap effectively.

Strategic positioning follows foundation work and involves creating sustainable competitive advantages through differentiation, specialization, or resource optimization. The most successful practitioners identify opportunities that align with their natural strengths while addressing genuine market needs that aren't being served effectively by existing alternatives.

Tactical execution requires translation of strategic concepts into daily activities that produce measurable progress toward defined objectives. This is where most people fail—they understand concepts intellectually but struggle to create systematic implementation that generates consi
  # Title page
    story.append(Paragraph(f"Professional Script: {topic}", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Word Count: {word_count} words | Speaking Time: ~{word_count//150} minutes", subtitle_style))
    story.append(Paragraph(f"Research Sources: {research_summary['total_sources']} sources analyzed", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(Spacer(1, 30))
    
    # Script content
    paragraphs = script_content.split('\n\n')
    for paragraph in paragraphs:
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), body_style))
            story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def enhanced_research_summary(topic, youtube_videos, articles):
    """Create comprehensive research summary"""
    summary = {
        'topic': topic,
        'total_sources': len(youtube_videos) + len(articles),
        'youtube_videos': len(youtube_videos),
        'articles': len(articles),
        'research_depth': 'Deep Research' if len(youtube_videos) + len(articles) > 30 else 'Standard Research',
        'top_channels': [],
        'top_sources': [],
        'content_themes': [],
        'research_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Analyze YouTube channels
    if youtube_videos:
        channel_stats = {}
        for video in youtube_videos:
            channel = video['channel']
            channel_stats[channel] = channel_stats.get(channel, 0) + 1
        summary['top_channels'] = sorted(channel_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Analyze article sources
    if articles:
        source_stats = {}
        for article in articles:
            source = article['source']
            source_stats[source] = source_stats.get(source, 0) + 1
        summary['top_sources'] = sorted(source_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return summary

# Enhanced Sidebar Configuration
st.sidebar.header("🎯 Million Dollar Script Configuration")
st.sidebar.markdown("---")

topic = st.sidebar.text_input(
    "🎬 Script Topic (Detailed):",
    placeholder="e.g., How to build a 7-figure online business using AI automation in 2024",
    help="Enter detailed topic for comprehensive research and script generation"
)

research_intensity = st.sidebar.selectbox(
    "🔍 Research Intensity:",
    [
        "Maximum Research (25 videos + 20 articles)",
        "Deep Research (20 videos + 15 articles)", 
        "Standard Research (15 videos + 12 articles)",
        "Quick Research (10 videos + 8 articles)"
    ]
)

script_specifications = st.sidebar.selectbox(
    "📝 Script Specifications:",
    [
        "Professional 30-Min (3000+ words)",
        "Extended 25-Min (2500+ words)",
        "Standard 20

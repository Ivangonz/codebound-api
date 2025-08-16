module Authentication
  include ActionController::Cookies
  extend ActiveSupport::Concern

  private

  def authenticate_user_with_jwt!
    raw = cookies.encrypted[:access_token]

    unless raw.present?
      Rails.logger.warn("JWT token missing from cookies")
      render json: { error: "token missing" }, status: :unauthorized and return
    end

    begin
      claims = JWT.decode(raw, ENV["JWT_SECRET"], true, { algorithm: "HS256" }).first
    rescue JWT::ExpiredSignature => e
      Rails.logger.warn("JWT expired signature: #{e.message}")
      render json: { error: "token expired" }, status: :unauthorized and return
    rescue JWT::DecodeError => e
      Rails.logger.warn("JWT decode error: #{e.message}")
      render json: { error: "invalid token" }, status: :unauthorized and return
    end

    @current_user_claims = claims
  end
end
